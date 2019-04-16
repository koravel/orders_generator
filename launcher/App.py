import os
import time
from datetime import datetime

from reporter.Repoter import Reporter
from tracking import ReportDataKeys
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
from serializer.proto.OrderRecord_pb2 import OrderRecord
from service.file.FileWriteService import FileWriteService
from service.message_broker.rabbitmq.RabbitMQService import RabbitMQService
from service.order.OrderRecordFileReadService import OrderFileReadService
from service.database.mysql.CRUDService import CRUDService
from tracking.ReportDataCollector import ReportDataCollector
from util import delete_excess_files
from util.connection.MySQLConnection import MySQLConnection
from util.connection.RabbitMQConnection import RabbitMQConnection


class App:
    __logger = None
    __path_provider = None
    __settings_provider = None
    __gen_settings_provider = None
    __thread_pool = None

    __mysql_service = None
    __rabbitmq_service = None
    __data_collector = None
    __reporter = None

    __exchange_name = ""
    __exchange_mode = ""
    __queues = ""

    __sql_batch_buffer = []
    __batch_amount = 0
    last_batch_amount = 0
    __whole_butches_amount = 0
    __mysql_butches_counter = 0

    @staticmethod
    def initialize():
        config = Config()
        log_distributor_builder = LogDistributorBuilder()
        default_log_distributor = log_distributor_builder.build_default()

        logger = Logger()
        logger.setup([default_log_distributor])

        App.__path_provider = PathProvider(logger=logger)

        config.pathes = App.__path_provider.load(load_default=True)

        App.__settings_provider = SettingsProvider(location=config.pathes[PathKeys.SETTINGS].location,
                                                   logger=logger)
        config.settings = App.__settings_provider.load()

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

        App.__gen_settings_provider = SettingsProvider(location=config.pathes[PathKeys.GEN_SETTINGS].location,
                                                       logger=logger)
        config.gen_settings = App.__gen_settings_provider.load()

        App.__logger = logger
        App.setup_services(config)
        App.setup_thread_pool(config)

        App.__data_collector = ReportDataCollector()
        App.__data_collector.setup()

        App.__reporter = Reporter(App.__data_collector.data)

        App.__batch_amount = config.gen_settings[GenSettingsKeys.portion_amount]

        if config.settings[SettingsKeys.system]["clear"]:
            from launcher import clear_services
            clear_services(config, logger)

        return config

    @staticmethod
    def setup_thread_pool(config):
        App.__thread_pool = ThreadPool(App.__logger)
        App.__thread_pool.setup(config.settings[SettingsKeys.system][SettingsKeys.threads_max])
        App.__thread_pool.add_data("consumed_messages", 0)

        consume_thread = TaskThread("rabbit_consuming", App.__thread_pool, App.__logger)
        mysql_thread = TaskThread("mysql_writing", App.__thread_pool, App.__logger)
        report_thread = TaskThread("reporting", App.__thread_pool, App.__logger)
        consume_thread.setup(task=App.__consuming)
        mysql_thread.setup(task=App.__writing_to_mysql)
        report_thread.setup(task=App.__reporting)
        App.__thread_pool.add_thead(thread=consume_thread)
        App.__thread_pool.add_thead(thread=mysql_thread)
        App.__thread_pool.add_thead(thread=report_thread)

    @staticmethod
    def setup_services(config):
        App.__rabbitmq_service = RabbitMQService(connection=RabbitMQConnection(
            host=config.settings[SettingsKeys.rabbit][SettingsKeys.host],
            port=config.settings[SettingsKeys.rabbit][SettingsKeys.port],
            vhost=config.settings[SettingsKeys.rabbit][SettingsKeys.vhost],
            user=config.settings[SettingsKeys.rabbit][SettingsKeys.user],
            password=config.settings[SettingsKeys.rabbit][SettingsKeys.password],
            logger=App.__logger
        ),
            logger=App.__logger)

        App.__exchange_name = config.settings[SettingsKeys.rabbit][SettingsKeys.order_record_config][SettingsKeys.exchange_name]
        App.__exchange_mode = config.settings[SettingsKeys.rabbit][SettingsKeys.order_record_config][SettingsKeys.exchange_mode]
        App.__queues = config.settings[SettingsKeys.rabbit][SettingsKeys.order_record_config][SettingsKeys.queues]

        App.__rabbitmq_service.declare_router(App.__exchange_name, App.__exchange_mode)

        for queue_name in App.__queues:
            App.__rabbitmq_service.declare_queue(queue_name)
            App.__rabbitmq_service.bind_queue(queue_name, App.__exchange_name, queue_name)

        App.__mysql_service = CRUDService(MySQLConnection(
            host=config.settings[SettingsKeys.mysql][SettingsKeys.host],
            port=config.settings[SettingsKeys.mysql][SettingsKeys.port],
            db=config.settings[SettingsKeys.mysql][SettingsKeys.database],
            user=config.settings[SettingsKeys.mysql][SettingsKeys.user],
            password=config.settings[SettingsKeys.mysql][SettingsKeys.password],
            logger=App.__logger
        ),
            keep_connection_open=config.settings[SettingsKeys.mysql][SettingsKeys.keep_connection_open],
            attempts=config.settings[SettingsKeys.mysql][SettingsKeys.connection_attempts],
            delay=config.settings[SettingsKeys.mysql][SettingsKeys.connection_attempts_delay],
            instant_connection_attempts=config.settings[SettingsKeys.mysql][SettingsKeys.instant_connection_attempts],
            logger=App.__logger
        )

    @staticmethod
    def generate(config):
        order_record_constructor = OrderRecordConstructor(config.gen_settings, App.__logger)
        order_record_constructor.setup_generators(
            x=config.gen_settings[GenSettingsKeys.x],
            y=config.gen_settings[GenSettingsKeys.y],
            a=config.gen_settings[GenSettingsKeys.a],
            c=config.gen_settings[GenSettingsKeys.c],
            m=config.gen_settings[GenSettingsKeys.m],
            t0=config.gen_settings[GenSettingsKeys.t0])

        order_record_sequence = order_record_constructor.get_sequence()

        records = []
        App.__thread_pool.add_data("order_records_amount", order_record_constructor.get_order_records_amount())

        order_records_amount = order_record_constructor.get_order_records_amount()

        App.__whole_butches_amount = int(order_records_amount / App.__batch_amount)

        App.last_batch_amount = order_records_amount - App.__whole_butches_amount * App.__batch_amount

        counter = App.__whole_butches_amount
        timer = datetime.now()
        for record in order_record_sequence:
            records.append(record)
            App.__data_collector.update_zone_data(timer, record.get_zone())
            if len(records) == App.__batch_amount and counter > 0:
                counter -= 1

                yield records
                records = []

            timer = datetime.now()

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

            App.__mysql_service.insert(location=config.settings[SettingsKeys.mysql][SettingsKeys.order_table], params=params)

    @staticmethod
    def to_proto(order_records):
        protos = []
        for order_record in order_records:
            protos.append(OrderRecordToProto.convert(order_record))

        return protos

    @staticmethod
    def to_rabbitmq(proto_records):
        for record in proto_records:
            App.__rabbitmq_service.send_message(App.__exchange_name, record.zone, record.SerializeToString())

    __order_fields = [
        "order_id",
        "status",
        "timestamp",
        "currency_pair",
        "direction",
        "init_price",
        "fill_price",
        "init_volume",
        "fill_volume",
        "tags",
        "description"
    ]

    @staticmethod
    def __consume_callback(ch, method, properties, body):
        App.__thread_pool.update_data("consumed_messages", App.__thread_pool.get_data("consumed_messages") + 1)
        App.__data_collector.set_data(ReportDataKeys.rabbit_consumed,
                                      App.__data_collector.get_data(ReportDataKeys.rabbit_consumed) + 1)
        order_record = OrderRecord()
        order_record.ParseFromString(body)
        values = [
            order_record.order_id,
            order_record.status,
            order_record.timestamp,
            order_record.currency_pair,
            order_record.direction,
            order_record.init_price,
            order_record.fill_price,
            order_record.init_volume,
            order_record.fill_volume,
            order_record.tags,
            order_record.description
        ]
        App.__sql_batch_buffer.append(values)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    __table = ""

    @staticmethod
    def get_db_info():
        from tracking import select_report_data_query
        return App.__mysql_service.execute_query(query=select_report_data_query, fetch=True)

    @staticmethod
    def __batch_to_mysql():
        try:
            App.__mysql_service.insert_many(location=App.__table, fields=App.__order_fields, values=App.__sql_batch_buffer[0:App.__batch_amount])
            App.__sql_batch_buffer = App.__sql_batch_buffer[App.__batch_amount:]
        except:
            App.__logger.log_error()
        else:

            db_info = App.get_db_info()
            App.__data_collector.set_data(ReportDataKeys.mysql_red, db_info[0][0] + db_info[0][1])
            App.__data_collector.set_data(ReportDataKeys.mysql_blue, db_info[0][2] + db_info[0][3])
            App.__data_collector.set_data(ReportDataKeys.mysql_green, db_info[0][4])
            App.__data_collector.set_data(ReportDataKeys.mysql_total, db_info[0][5])

    @staticmethod
    def __writing_to_mysql(events, data, logger):
        while True:
            time.sleep(0.5)
            if len(App.__sql_batch_buffer) > 0:
                App.__batch_to_mysql()

    @staticmethod
    def start_writing_to_mysql(config):
        App.__table = config.settings[SettingsKeys.mysql][SettingsKeys.order_table]
        App.__thread_pool.start_thread("mysql_writing")

    @staticmethod
    def start_rabbit_consuming():
        for queue_name in App.__queues:
            App.__rabbitmq_service.consume_message(queue_name=queue_name, on_consume_callback=App.__consume_callback)

        App.__thread_pool.start_thread("rabbit_consuming")

    @staticmethod
    def start_reporting():
        App.__thread_pool.start_thread("reporting")

    @staticmethod
    def __reporting(events, data, logger):
        while True:
            time.sleep(5)
            App.report()

    @staticmethod
    def __consuming(events, data, logger):
        App.__mysql_butches_counter = App.__whole_butches_amount
        App.__rabbitmq_service.start_consuming()

    @staticmethod
    def report():

        result = App.__reporter.get_report()

        App.__logger.log_info(result)

    @staticmethod
    def finalize(config):
        for thread_name in App.__thread_pool.get_threads().keys():
            App.__thread_pool.join_thread(thread_name)
        App.__path_provider.save(config.pathes)
        App.__settings_provider.save(config.settings)
        App.__gen_settings_provider.save(config.gen_settings)
