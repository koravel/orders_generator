import config.PathProvider
import services.json as sjson

settings = dict()


def save(write=sjson.write):
    global settings
    try:
        write(settings, PathProvider.pathes["SETTINGS"].location)
    except Exception as ex:
        raise ex


def load(read=sjson.read):
    global settings
    try:
        settings = read(PathProvider.pathes["SETTINGS"].location)
    except Exception as ex:
        set_defaults(read)
        raise ex


def set_defaults(read=sjson.read):
    global settings
    settings = read(PathProvider.pathes["DEFAULT_SETTINGS"].location)
