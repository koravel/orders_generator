import os

from config.provider.Path import Path
from config.provider import PathKeys
from config import get_root_location
import config
from config.provider.Provider import Provider
from serializer.PathEncoder import PathEncoder
from serializer.PathDecoder import PathDecoder
from service.json.JSONReadService import JSONReadService
from service.json.JSONWriteService import JSONWriteService


class PathProvider(Provider):
    def __init__(self, location=config.get_pathes_config_location(), default_location=None, logger=None):
        self.location = location
        self.default_location = default_location
        self.logger = logger

        self.__root_location = get_root_location()
        self.__default_pathes = {
            PathKeys.ROOT: Path(self.__root_location),
            PathKeys.LOG: Path(os.path.join(self.__root_location, "log")),
            PathKeys.SETTINGS: Path(os.path.join(self.__root_location, "settings.json")),
            PathKeys.GEN_SETTINGS: Path(os.path.join(self.__root_location, "gen-settings.json")),
            PathKeys.DEFAULT_SETTINGS: Path(os.path.join(self.__root_location, "settings-default.json")),
            PathKeys.DEFAULT_GEN_SETTINGS: Path(os.path.join(self.__root_location, "gen-settings-default.json")),
            PathKeys.GEN_OUT: Path(os.path.join(self.__root_location, "out"))
        }

    def load(self, read_method=JSONReadService.read):
        """
         Load pathes dictionary based on root file location, by default PathProvider.py
        """
        pathes = dict()
        try:
            if os.path.exists(self.location):
                pathes = read_method(self.location, PathDecoder)
                if pathes is None:
                    pathes = self.__set_to_defaults()
                else:
                    self.__create_pathes(pathes)
            else:
                pathes = self.__set_to_defaults()
        except:
            if self.logger is not None:
                self.logger.log_fatal("Error while loading PathProvider", include_traceback=True)
        else:
            if self.logger is not None:
                self.logger.log_info("Pathes loaded sucessfully")
        return pathes

    def save(self, pathes, write=JSONWriteService.write):
        """
        Save pathes to .json file
        """
        try:
            write(pathes, self.location, PathEncoder)
        except:
            if self.logger is not None:
                self.logger.log_critical("Error while saving PathProvider", include_traceback=True)
        else:
            if self.logger is not None:
                self.logger.log_info("Pathes saved sucessfully")

    def __set_to_defaults(self):
        """
        Set app pathes to default
        """
        return self.__default_pathes

    @staticmethod
    def __create_pathes(pathes):
        """
        Crates pathes if they does not exists in file system
        """
        for key, path in pathes.items():

            if not os.path.exists(path.location):
                basename = os.path.basename(path.location)
                if basename.__contains__('.'):
                    if not basename.__contains__(".tab"):
                        open(path.location, "x").close()
                else:
                    os.mkdir(path.location)
