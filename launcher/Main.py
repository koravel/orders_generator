from config.provider import PathKeys
from config.Config import Config
from logging.Logger import Logger
from config.provider.SettingsProvider import SettingsProvider
from config.provider.PathProvider import PathProvider
from service.file.FileWriteService import FileWriteService


class Main:
    @staticmethod
    def initialize():
        Main.config = Config()
        Main.logger = Logger()
        Main.path_provider = PathProvider(logger=Main.logger)
        Main.logger.setup(append_method=FileWriteService.write, location=None, enable_startup_caching=True)
        Main.config.pathes = Main.path_provider.load()

        Main.logger.setup(append_method=FileWriteService.write, location= Main.config.pathes[PathKeys.LOG].location)

        Main.settings_provider = SettingsProvider(location=Main.config.pathes[PathKeys.SETTINGS].location,
                                             default_location= Main.config.pathes[PathKeys.DEFAULT_SETTINGS].location,
                                             logger=Main.logger)
        Main.config.settings = Main.settings_provider.load()

        Main.gen_settings_provider = SettingsProvider(location=Main.config.pathes[PathKeys.GEN_SETTINGS].location,
                                                  default_location=Main.config.pathes[
                                                      PathKeys.DEFAULT_GEN_SETTINGS].location,
                                                  logger=Main.logger)
        Main.config.gen_settings = Main.gen_settings_provider.load()

    @staticmethod
    def run():
        pass

    @staticmethod
    def finalize():
        Main.path_provider.save(Main.config.pathes)
        Main.settings_provider.save(Main.config.settings)
        Main.gen_settings_provider.save(Main.config.gen_settings)


if __name__ == "__main__":
    Main.initialize()
    Main.run()
    Main.finalize()
