from service.json.JSONWriteService import JSONWriteService
from service.json.JSONReadService import JSONReadService
from config.Config import Config
from config.Provider import Provider


class SettingsProvider(Provider):
    @staticmethod
    def save(location, write_method=JSONWriteService.write, logger=None):
        try:
            write_method(Config.settings, location)
        except:
            if logger is not None:
                logger.log_critical("Cannot save settings. Any changes were lost", include_traceback=True)

    @staticmethod
    def load(location, default_location=None, read_method=JSONReadService.read, logger=None):
        try:
            Config.settings = read_method(location)
        except:
            if default_location is not None:
                if logger is not None:
                    logger.log_critical("Cannot load settings. Try to load default file...", include_traceback=True)
                SettingsProvider.__load_defaults(read_method)

    @staticmethod
    def __load_defaults(location, read=JSONReadService.read, logger=None):
        try:
            Config.settings = read(location)
        except:
            if logger is not None:
                logger.log_critical("Unable to load default settings", include_traceback=True)
