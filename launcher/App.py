import os
from datetime import datetime

from config.provider import PathKeys
from config.provider import GenSettingsKeys
from config.provider import SettingsKeys
from config.Config import Config
from generator.OrderConstructor import OrderConstructor
from logging.Logger import Logger
from config.provider.SettingsProvider import SettingsProvider
from config.provider.PathProvider import PathProvider
from service.file.FileWriteService import FileWriteService
from util import delete_excess_files


class App:
    @staticmethod
    def initialize():
        config = Config()
        logger = Logger()
        path_provider = PathProvider(logger=logger)

        logger.setup(append_method=FileWriteService.append, location=None, enable_startup_caching=True)
        config.pathes = path_provider.load()

        logger.setup(append_method=FileWriteService.append, location=config.pathes[PathKeys.LOG].location, log_level=6)

        settings_provider = SettingsProvider(location=config.pathes[PathKeys.SETTINGS].location,
                                             default_location= config.pathes[PathKeys.DEFAULT_SETTINGS].location,
                                             logger=logger)
        config.settings = settings_provider.load()

        delete_excess_files(
            config.pathes[PathKeys.GEN_OUT].location,
            config.settings[SettingsKeys.system][SettingsKeys.out_files_max],
            logger)

        delete_excess_files(
            config.pathes[PathKeys.LOG].location,
            config.settings[SettingsKeys.system][SettingsKeys.logger_files_max],
            logger)

        logger.log_level = config.settings[SettingsKeys.system][SettingsKeys.log_level]

        gen_settings_provider = SettingsProvider(location=config.pathes[PathKeys.GEN_SETTINGS].location,
                                                  default_location=config.pathes[
                                                      PathKeys.DEFAULT_GEN_SETTINGS].location,
                                                  logger=logger)
        config.gen_settings = gen_settings_provider.load()

        return config, logger, path_provider, settings_provider, gen_settings_provider

    @staticmethod
    def generate(config, logger):
        order_constructor = OrderConstructor(config.gen_settings, logger)
        order_constructor.setup_generators(
            x=config.gen_settings[GenSettingsKeys.x],
            y=config.gen_settings[GenSettingsKeys.y],
            a=config.gen_settings[GenSettingsKeys.a],
            c=config.gen_settings[GenSettingsKeys.c],
            m=config.gen_settings[GenSettingsKeys.m],
            t0=config.gen_settings[GenSettingsKeys.t0])

        order_sequence = order_constructor.get_sequence()

        for order in order_sequence:
            yield order

    @staticmethod
    def to_file(config, orders):
        file = "{}.out".format(datetime.now().replace(microsecond=0)).replace(":", "_")
        FileWriteService.append_array(orders,
                               os.path.join(config.pathes[PathKeys.GEN_OUT].location, file))

    @staticmethod
    def finalize(config, path_provider, settings_provider, gen_settings_provider):
        path_provider.save(config.pathes)
        settings_provider.save(config.settings)
        gen_settings_provider.save(config.gen_settings)
