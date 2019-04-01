import os
import traceback

import config
from config.Config import Config
from config.Provider import Provider
from serializer.PathEncoder import PathEncoder
from serializer.PathDecoder import PathDecoder
from service.json.JSONReadService import JSONReadService
from service.json.JSONWriteService import JSONWriteService


class PathProvider(Provider):
    @staticmethod
    def load(location, default_location, read_method=JSONReadService.read, logger=None):
        """
         Load pathes dictionary based on root file location, by default PathProvider.py
        """
        try:
            pathes_location = PathProvider.__get_pathes_config_location()
            if os.path.exists(pathes_location):
                Config.pathes = read_method(pathes_location, PathDecoder)
                if Config.pathes is None:
                    PathProvider.__set_to_defaults()
                else:
                    PathProvider.__create_pathes()
            else:
                PathProvider.__set_to_defaults()
        except:
            logger.log_fatal("Error while loading PathProvider")
            logger.log_fatal(traceback.format_exc())

    @staticmethod
    def save(write=JSONWriteService.write, logger=None):
        """
        Save pathes to .json file
        """
        try:
            write(Config.pathes, PathProvider.__get_pathes_config_location(), PathEncoder)
        except:
            logger.log_critical("Error while saving PathProvider")
            logger.log_critical(traceback.format_exc())

    @staticmethod
    def __set_to_defaults():
        """
        Set app pathes to default
        """
        Config.pathes = Config.default_pathes

    @staticmethod
    def __create_pathes():
        """
        Crates pathes if they does not exists in file system
        """
        for key, path in Config.pathes.items():

            if not os.path.exists(path.location):
                basename = os.path.basename(path.location)
                if basename.__contains__('.'):
                    if not basename.__contains__(".tab"):
                        open(path.location, "x").close()
                else:
                    os.mkdir(path.location)

    @staticmethod
    def __get_pathes_config_location():
        return os.path.join(config.root_location, config.pathes_file_name)
