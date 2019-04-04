import os

from config.provider import PathKeys
from config.provider import GenSettingsKeys
from config.provider import SettingsKeys
from config.Config import Config
from converter.OrderRecordToProto import OrderRecordToProto
from generator.OrderRecordConstructor import OrderRecordConstructor
from llogging.LogDistributorBuilder import LogDistributorBuilder
from llogging.Logger import Logger
from config.provider.SettingsProvider import SettingsProvider
from config.provider.PathProvider import PathProvider
from service.file.FileWriteService import FileWriteService
from service.message_broker.rabbitmq.RabbitMQService import RabbitMQService
from service.order.OrderRecordFileReadService import OrderFileReadService
from service.order.OrderMySQLService import OrderMySQLService
from util import delete_excess_files
from util.connection.MySQLConnection import MySQLConnection
from util.connection.RabbitMQConnection import RabbitMQConnection


class App:
    @staticmethod
    def initialize():
        config = Config()
        log_distributor_builder = LogDistributorBuilder()
        default_log_distributor = log_distributor_builder.build_default()

        logger = Logger()
        logger.setup([default_log_distributor])

        path_provider = PathProvider(logger=logger)

        config.pathes = path_provider.load()

        settings_provider = SettingsProvider(location=config.pathes[PathKeys.SETTINGS].location,
                                             default_location=config.pathes[PathKeys.DEFAULT_SETTINGS].location,
                                             logger=logger)
        config.settings = settings_provider.load()

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

        gen_settings_provider = SettingsProvider(location=config.pathes[PathKeys.GEN_SETTINGS].location,
                                                 default_location=config.pathes[
                                                     PathKeys.DEFAULT_GEN_SETTINGS].location,
                                                 logger=logger)
        config.gen_settings = gen_settings_provider.load()

        return config, logger, path_provider, settings_provider, gen_settings_provider

    @staticmethod
    def generate(config, logger):
        order_record_constructor = OrderRecordConstructor(config.gen_settings, logger)
        order_record_constructor.setup_generators(
            x=config.gen_settings[GenSettingsKeys.x],
            y=config.gen_settings[GenSettingsKeys.y],
            a=config.gen_settings[GenSettingsKeys.a],
            c=config.gen_settings[GenSettingsKeys.c],
            m=config.gen_settings[GenSettingsKeys.m],
            t0=config.gen_settings[GenSettingsKeys.t0])

        order_record_sequence = order_record_constructor.get_sequence()

        records = []
        for record in order_record_sequence:

            records.append(record)
        return records

    @staticmethod
    def to_file(config, orders, file_name):
        for order in orders:
            FileWriteService.append(order, os.path.join(config.pathes[PathKeys.GEN_OUT].location, file_name))

    @staticmethod
    def from_file(config, file_name):
        orders = OrderFileReadService.read_all(os.path.join(config.pathes[PathKeys.GEN_OUT].location, file_name))

        return orders

    @staticmethod
    def to_mysql(config, logger, order_records):
        mysql_service = OrderMySQLService(MySQLConnection(
            host=config.settings[SettingsKeys.mysql][SettingsKeys.host],
            port=config.settings[SettingsKeys.mysql][SettingsKeys.port],
            db=config.settings[SettingsKeys.mysql][SettingsKeys.database],
            user=config.settings[SettingsKeys.mysql][SettingsKeys.user],
            password=config.settings[SettingsKeys.mysql][SettingsKeys.password],
            logger=logger
        ),
            keep_connection_open=True,
            logger=logger
        )
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

            mysql_service.insert(config.settings[SettingsKeys.mysql][SettingsKeys.order_table], params)

    @staticmethod
    def to_proto(order_records):
        protos = []
        for order_record in order_records:
            protos.append(OrderRecordToProto.convert(order_record))

        return protos

    @staticmethod
    def to_rabbitmq(config, logger, proto_records):
        rabbitmq = RabbitMQService(connection=RabbitMQConnection(
            host=config.settings[SettingsKeys.rabbit][SettingsKeys.host],

            vhost=config.settings[SettingsKeys.rabbit][SettingsKeys.vhost],
            user=config.settings[SettingsKeys.rabbit][SettingsKeys.user],
            password=config.settings[SettingsKeys.rabbit][SettingsKeys.password],
            logger=logger
        ),
            logger=logger)

        rabbitmq.declare_queue("red")
        rabbitmq.declare_queue("green")
        rabbitmq.declare_queue("blue")

        rabbitmq.declare_router("proto_exchange", "direct")

        rabbitmq.bind_queue("red", "proto_exchange", "red")
        rabbitmq.bind_queue("green", "proto_exchange", "green")
        rabbitmq.bind_queue("blue", "proto_exchange", "blue")

        for record in proto_records:
            rabbitmq.send_message("proto_exchange", record.zone, record.SerializeToString())

    @staticmethod
    def report(logger, timings, proto_records):

        zone_counts = {
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
                                ))

    @staticmethod
    def finalize(config, path_provider, settings_provider, gen_settings_provider):
        path_provider.save(config.pathes)
        settings_provider.save(config.settings)
        gen_settings_provider.save(config.gen_settings)
