import json
import os

import root


class PathKeys:
    ROOT = "ROOT",
    LOG = "LOG",
    SETTINGS = "SETTINGS",
    CONSTANTS = "CONSTANTS",
    DEFAULT_SETTINGS = "DEFAULT_SETTINGS",
    DEFAULT_CONSTANTS = "DEFAULT_CONSTANTS",
    GEN_OUT = "GEN_OUT"


class Config:
    settings = dict()
    pathes = dict()

    __root_location = root.__file__
    pathes_file_name = "pathes.json"
    default_pathes = {
        PathKeys.ROOT: __root_location,
        PathKeys.LOG: os.path.join(__root_location, "log"),
        PathKeys.SETTINGS: os.path.join(__root_location, "settings.json"),
        PathKeys.CONSTANTS: os.path.join(__root_location, "constants.json"),
        PathKeys.DEFAULT_SETTINGS: os.path.join(__root_location, "constants-default.json"),
        PathKeys.DEFAULT_CONSTANTS: os.path.join(__root_location, "settings-default.json"),
        PathKeys.GEN_OUT: os.path.join(__root_location, "out")
    }


class Path:
    def __init__(self, _location, _is_remote=False):
        self.location = _location
        self.is_remote = _is_remote

    def isoformat(self):
        """
        Rewrite default 'to json'-method
        """
        return {"location": self.location, "is_remote": self.is_remote}


# override JSON encoder for PathProvider data structure
class PathEncoder(json.JSONEncoder):
    def default(self, o):
        """
         Rewrite default encode method of Path object
        """
        if isinstance(o, Path):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


# override JSON decoder for PathProvider data structure
class PathDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(obj):
        """
         Rewrite default decode method of Path object
        """
        if 'location' in obj:
            return Path(obj.get('location'), obj.get('is_remote'))
        return obj
