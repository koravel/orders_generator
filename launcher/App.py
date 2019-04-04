import os

from config.provider import PathKeys
from config.provider import GenSettingsKeys
from config.provider import SettingsKeys
from config.Config import Config
from generator.OrderConstructor import OrderConstructor
from generator.OrderRecordConstructor import OrderRecordConstructor
from logging.LogDistributorBuilder import LogDistributorBuilder
from logging.Logger import Logger
from config.provider.SettingsProvider import SettingsProvider
from config.provider.PathProvider import PathProvider
from service.file.FileWriteService import FileWriteService
from service.order.OrderRecordFileReadService import OrderFileReadService
from service.order.OrderMySQLService import OrderMySQLService
from util import delete_excess_files
from util.connection.MySQLConnection import MySQLConnection


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
    def to_mysql(config, logger, orders):
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
        for order in orders:
            params = {
                "fields":{
                    "order_id",
                    "timestamp",
                    "currency_pair",
                    "order_direction",
                    "init_price",
                    "fill_price",
                    "init_volume",
                    "fill_volume",
                    "description",
                    "tags"
                },
                "values":{
                    order.id
                    }
            }
            mysql_service.insert(config.settings[SettingsKeys.mysql][SettingsKeys.order_table], params)

    @staticmethod
    def finalize(config, path_provider, settings_provider, gen_settings_provider):
        path_provider.save(config.pathes)
        settings_provider.save(config.settings)
        gen_settings_provider.save(config.gen_settings)

    # @staticmethod
    # def __get_out_file_name():
