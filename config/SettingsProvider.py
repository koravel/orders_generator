from service.json.JSONWriteService import JSONWriteService
from service.json.JSONReadService import JSONReadService
from config import Config, PathKeys


class SettingsProvider:
    @staticmethod
    def save(write=JSONWriteService.write):
        try:
            write(Config.settings, Config.pathes[PathKeys.SETTINGS].location)
        except Exception as ex:
            raise ex

    @staticmethod
    def load(read=JSONReadService.read):
        try:
            Config.settings = read(Config.pathes[PathKeys.SETTINGS].location)
        except Exception as ex:
            SettingsProvider.load_defaults(read)
            raise ex

    @staticmethod
    def load_defaults(read=JSONReadService.read):
        Config.settings = read(Config.pathes[PathKeys.DEFAULT_SETTINGS].location)
