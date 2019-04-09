import os

from app_threading.TaskThread import TaskThread
from app_threading.ThreadPool import ThreadPool
from config.provider import PathKeys
from config.provider import GenSettingsKeys
from config.provider import SettingsKeys
from config.Config import Config
from converter.OrderRecordToProto import OrderRecordToProto
from generator.OrderRecordConstructor import OrderRecordConstructor
from app_logging.LogDistributorBuilder import LogDistributorBuilder
from app_logging.Logger import Logger
from config.provider.SettingsProvider import SettingsProvider
from config.provider.PathProvider import PathProvider
from proto.OrderRecord_pb2 import OrderRecord
from service.file.FileWriteService import FileWriteService
from service.message_broker.rabbitmq.RabbitMQService import RabbitMQService
from service.order.OrderRecordFileReadService import OrderFileReadService
from service.database.mysql.CRUDService import CRUDService
from util import delete_excess_files
from util.connection.MySQLConnection import MySQLConnection
from util.connection.RabbitMQConnection import RabbitMQConnection


class App:
    logger = None
    path_provider = None
    settings_provider = None
    gen_settings_provider = None
    thread_pool = None

    mysql_service = None
    rabbitmq_service = None

    red_queue = "red"
    green_queue = "green"
    blue_queue = "blue"
    exchange_name = "order_records"
    exchange_mode = "direct"

    __table = ""

    @staticmethod
    def initialize():
        config = Config()
        log_distributor_builder = LogDistributorBuilder()
        default_log_distributor = log_distributor_builder.build_default()

        logger = Logger()
        logger.setup([default_log_distributor])

        App.path_provider = PathProvider(logger=logger)

        config.pathes = App.path_provider.load(load_default=True)

        App.settings_provider = SettingsProvider(location=config.pathes[PathKeys.SETTINGS].location,
                                             logger=logger)
        config.settings = App.settings_provider.load()

        log_distributor_builder.setup(config.settings[SettingsKeys.logging][SettingsKeys.loggers])
        log_distributors = log_distributor_builder.build_all()

        logger.setup(log_distributors=log_distributors)

        delete_excess_files(
            config.pathes[PathKeys.GEN_OUT].location,
            config.settings[SettingsKeys.system][SettingsKeys.out_files_max],
            logger)

        delete_excess_files(
            config.pathes[PathKeys.LOG].location,
            config.settings[SettingsKeys.logging][SettingsKeys.logger_files_max],
            logger)

        App.gen_settings_provider = SettingsProvider(location=config.pathes[PathKeys.GEN_SETTINGS].location,
                                                 logger=logger)
        config.gen_settings = App.gen_settings_provider.load()

        App.logger = logger
        App.setup_services(config)
        App.setup_thread_pool(config)

        return config

    @staticmethod
    def setup_thread_pool(config):
        App.thread_pool = ThreadPool(App.logger)
        App.thread_pool.setup(config.settings[SettingsKeys.system][SettingsKeys.threads_max])
        App.thread_pool.add_data("consumed_messages", 0)

        thread = TaskThread("rabbit_consuming", App.thread_pool, App.logger)
        thread.setup(task=App.__consuming)
        App.thread_pool.add_thead(thread=thread)

    @staticmethod
    def setup_services(config):
        App.rabbitmq_service = RabbitMQService(connection=RabbitMQConnection(
            host=config.settings[SettingsKeys.rabbit][SettingsKeys.host],
            port=config.settings[SettingsKeys.rabbit][SettingsKeys.port],
            vhost=config.settings[SettingsKeys.rabbit][SettingsKeys.vhost],
            user=config.settings[SettingsKeys.rabbit][SettingsKeys.user],
            password=config.settings[SettingsKeys.rabbit][SettingsKeys.password],
            logger=App.logger
        ),
            logger=App.logger)

        App.rabbitmq_service.declare_queue(App.red_queue)
        App.rabbitmq_service.declare_queue(App.green_queue)
        App.rabbitmq_service.declare_queue(App.blue_queue)

        App.rabbitmq_service.declare_router(App.exchange_name, App.exchange_mode)

        App.rabbitmq_service.bind_queue(App.red_queue, App.exchange_name, App.red_queue)
        App.rabbitmq_service.bind_queue(App.green_queue, App.exchange_name, App.green_queue)
        App.rabbitmq_service.bind_queue(App.blue_queue, App.exchange_name, App.blue_queue)

        App.mysql_service = CRUDService(MySQLConnection(
            host=config.settings[SettingsKeys.mysql][SettingsKeys.host],
            port=config.settings[SettingsKeys.mysql][SettingsKeys.port],
            db=config.settings[SettingsKeys.mysql][SettingsKeys.database],
            user=config.settings[SettingsKeys.mysql][SettingsKeys.user],
            password=config.settings[SettingsKeys.mysql][SettingsKeys.password],
            logger=App.logger
        ),
            keep_connection_open=config.settings[SettingsKeys.mysql][SettingsKeys.keep_connection_open],
            attempts=config.settings[SettingsKeys.mysql][SettingsKeys.connection_attempts],
            delay=config.settings[SettingsKeys.mysql][SettingsKeys.connection_attempts_delay],
            instant_connection_attempts=config.settings[SettingsKeys.mysql][SettingsKeys.instant_connection_attempts],
            logger=App.logger
        )

    @staticmethod
    def generate(config):
        order_record_constructor = OrderRecordConstructor(config.gen_settings, App.logger)
        order_record_constructor.setup_generators(
            x=config.gen_settings[GenSettingsKeys.x],
            y=config.gen_settings[GenSettingsKeys.y],
            a=config.gen_settings[GenSettingsKeys.a],
            c=config.gen_settings[GenSettingsKeys.c],
            m=config.gen_settings[GenSettingsKeys.m],
            t0=config.gen_settings[GenSettingsKeys.t0])

        order_record_sequence = order_record_constructor.get_sequence()

        records = []
        App.thread_pool.add_data("order_records_amount", order_record_constructor.get_order_records_amount())
        counter = order_record_constructor.get_order_records_amount() / config.gen_settings[GenSettingsKeys.portion_amount]
        for record in order_record_sequence:
            records.append(record)
            if len(records) == config.gen_settings[GenSettingsKeys.portion_amount] and counter > 0:
                counter -= 1
                yield records
                records = []

        if len(records) > 0:
            yield records

    @staticmethod
    def to_file(config, orders, file_name):
        for order in orders:
            FileWriteService.append(order, os.path.join(config.pathes[PathKeys.GEN_OUT].location, file_name))

    @staticmethod
    def from_file(config, file_name):
        orders = OrderFileReadService.read_all(os.path.join(config.pathes[PathKeys.GEN_OUT].location, file_name))

        return orders

    @staticmethod
    def to_mysql(config, order_records):
        for order_record in order_records:
            params = {
                "id": order_record.get_id(),
                "order_id": order_record.order.get_id(),
                "status": order_record.get_status(),
                "timestamp": order_record.get_timestamp(),
                "currency_pair": order_record.order.get_currency_pair(),
                "direction": order_record.order.get_direction(),
                "init_price": order_record.order.get_init_price(),
                "fill_price": order_record.get_fill_price(),
                "init_volume": order_record.order.get_init_volume(),
                "fill_volume": order_record.get_fill_volume(),
                "tags": order_record.order.get_tags(),
                "description": order_record.order.get_description()
                }

            App.mysql_service.insert(location=config.settings[SettingsKeys.mysql][SettingsKeys.order_table], params=params)

    @staticmethod
    def to_proto(order_records):
        protos = []
        for order_record in order_records:
            protos.append(OrderRecordToProto.convert(order_record))

        return protos

    @staticmethod
    def to_rabbitmq(proto_records):
        for record in proto_records:
            App.rabbitmq_service.send_message(App.exchange_name, record.zone, record.SerializeToString())

    @staticmethod
    def mysql_callback(ch, method, properties, body):
        App.thread_pool.update_data("consumed_messages", App.thread_pool.get_data("consumed_messages") + 1)
        order_record = OrderRecord()
        order_record.ParseFromString(body)
        params = {
            "id": order_record.id,
            "order_id": order_record.order_id,
            "status": order_record.status,
            "timestamp": order_record.timestamp,
            "currency_pair": order_record.currency_pair,
            "direction": order_record.direction,
            "init_price": order_record.init_price,
            "fill_price": order_record.fill_price,
            "init_volume": order_record.init_volume,
            "fill_volume": order_record.fill_volume,
            "tags": order_record.tags,
            "description": order_record.description
        }
        try:
            App.mysql_service.insert(location=App.__table, params=params)
        except:
            App.logger.log_error()
        else:
            if App.thread_pool.get_data("consumed_messages") >= App.thread_pool.get_data("order_records_amount"):
                App.rabbitmq_service.stop_consuming()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def from_rabbit_to_mysql(config):
        App.__table = config.settings[SettingsKeys.mysql][SettingsKeys.order_table]

        for queue_name in [App.red_queue, App.green_queue, App.blue_queue]:
            App.rabbitmq_service.consume_message(queue_name=queue_name, on_consume_callback=App.mysql_callback)

        App.thread_pool.start_thread("rabbit_consuming")

    @staticmethod
    def __consuming(events, data, logger):
        App.rabbitmq_service.start_consuming()

    @staticmethod
    def report(logger, timings, proto_records):
        pass
        """zone_counts = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }

        for record in proto_records:
            if record.zone == "red":
                zone_counts["red"] += 1
            elif record.zone == "green":
                zone_counts["green"] += 1
            elif record.zone == "blue":
                zone_counts["blue"] += 1

        logger.log_info("\n=======REPORT=======\n"
                        "Order records in:\n"
                        "Red zone:{}\n"
                        "Green zone:{}\n"
                        "Blue zone:{}\n"
                        "Setup time:{}\n"
                        "Generation time:{}\n"
                        "Write to file time:{}\n"
                        "Read from file time:{}\n"
                        "Write to MySQL DB time:{}\n"
                        "Convert to proto time:{}\n"
                        "Send to RabbitMQ time:{}\n"
                        "\n=====END=REPORT=====\n"
                        .format(zone_counts["red"], zone_counts["green"], zone_counts["blue"],
                                timings["setup"],
                                timings["gen"],
                                timings["to_file"],
                                timings["from_file"],
                                timings["mysql"],
                                timings["proto"],
                                timings["rabbit"]
                                ))"""

    @staticmethod
    def finalize(config):
        App.path_provider.save(config.pathes)
        App.settings_provider.save(config.settings)
        App.gen_settings_provider.save(config.gen_settings)
