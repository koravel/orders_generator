import os
import json
import traceback

import services.json as sjson


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

    def object_hook(self, obj):
        """
         Rewrite default decode method of Path object
        """
        if 'location' in obj:
            return Path(obj.get('location'), obj.get('is_remote'))
        return obj


__pathes__file_name = "pathes.json"
pathes = dict()


def __set_to_defaults(root_location):
    """
    Set app pathes to default
    """
    global pathes
    pathes["LOG"] = Path(os.path.join(root_location, "log"))
    pathes["SETTINGS"] = Path(os.path.join(root_location, "settings.json"))
    pathes["CONSTANTS"] = Path(os.path.join(root_location, "constants.json"))
    pathes["DEFAULT_CONSTANTS"] = Path(os.path.join(root_location, "constants-default.json"))
    pathes["DEFAULT_SETTINGS"] = Path(os.path.join(root_location, "settings-default.json"))
    pathes["GEN_OUT"] = Path(os.path.join(root_location, "out"))
    save()


def __create_pathes():
    global pathes
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
    save()


def load(root=__file__):
    """
     Load pathes dictionary based on root file location, by default PathProvider.py
    """
    global pathes
    try:
        pathes["ROOT"] = Path(os.path.dirname(os.path.abspath(root)))
        root_location = pathes["ROOT"].location
        pathes_location = os.path.join(pathes["ROOT"].location, __pathes__file_name)
        if os.path.exists(pathes_location):
            pathes = sjson.read(pathes_location, PathDecoder)
            if pathes is None:
                __set_to_defaults(root_location)
            else:
                __create_pathes()
        else:
            __set_to_defaults(root_location)
    except:
        print("Error while loading PathProvider")
        print(traceback.format_exc())


def save():
    """
    Save pathes to .json file
    """
    try:
        sjson.write(pathes, os.path.join(pathes["ROOT"].location, __pathes__file_name), PathEncoder)
    except:
        print("Error while saving PathProvider")
        print(traceback.format_exc())

