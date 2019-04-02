from service.json.JSONWriteService import JSONWriteService
from service.json.JSONReadService import JSONReadService
from config.provider.Provider import Provider


class SettingsProvider(Provider):
    def save(self, settings, write_method=JSONWriteService.write):
        try:
            write_method(settings, self.location)
        except:
            self.logger.log_critical("Cannot save settings. Any changes were lost", include_traceback=True)

    def load(self, read_method=JSONReadService.read):
        settings = dict()
        try:
            settings = read_method(self.location)
        except:
            if self.default_location is not None:
                self.__log_error("Cannot load settings. Try to load default file...")
                settings = self.__load_defaults(read_method)
        return settings

    def __load_defaults(self, read_method=JSONReadService.read):
        try:
            return read_method(self.default_location)
        except:
            self.__log_error("Unable to load default settings")

    def __log_error(self, text):
        if self.logger is not None:
            self.logger.log_critical(text, include_traceback=True)
