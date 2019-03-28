import os
import traceback

from config import PathKeys
from config.Config import Config
from serializer.PathEncoder import PathEncoder
from serializer.PathDecoder import PathDecoder
from service.json.JSONReadService import JSONReadService
from service.json.JSONWriteService import JSONWriteService


class PathProvider:
    @staticmethod
    def load():
        """
         Load pathes dictionary based on root file location, by default PathProvider.py
        """
        try:
            pathes_location = os.path.join(Config.pathes[PathKeys.ROOT].location, Config.pathes_file_name)
            if os.path.exists(pathes_location):
                Config.pathes = JSONReadService.read(pathes_location, PathDecoder)
                if Config.pathes is None:
                    PathProvider.__set_to_defaults()
                else:
                    PathProvider.__create_pathes()
            else:
                PathProvider.__set_to_defaults()
        except:
            print("Error while loading PathProvider")
            print(traceback.format_exc())

    @staticmethod
    def save():
        """
        Save pathes to .json file
        """
        try:
            JSONWriteService.write(Config.pathes, os.path.join(Config.pathes[PathKeys.ROOT].location,
                                                               Config.pathes_file_name), PathEncoder)
        except:
            print("Error while saving PathProvider")
            print(traceback.format_exc())

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
