from config import PathKeys
from config.Config import Config
from generator.constant.GenConfig import GenConfig
from service.json.JSONReadService import JSONReadService as jsonrs
from config.Provider import Provider


class OrderGenConstantsProvider(Provider):
    @staticmethod
    def load(read=jsonrs.read, logger=None):
        try:
            GenConfig.constants = read(Config.pathes[PathKeys.CONSTANTS].location)

        except Exception as ex:
            OrderGenConstantsProvider.__set_defaults(read)
            raise ex

    @staticmethod
    def save(write, logger):
        pass

    @staticmethod
    def __set_defaults(read=jsonrs.read):
        GenConfig.constants = read(Config.pathes[PathKeys.DEFAULT_CONSTANTS].location)
