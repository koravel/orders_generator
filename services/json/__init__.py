import json
import services.file as sf


def encode(obj, extended_encoder=None):
    try:
        result = json.dumps(obj=obj, sort_keys=True, indent=4, cls=extended_encoder)
    except Exception as ex:
        return ex
    else:
        return result


def decode(obj, extended_decoder=None):
    try:
        result = json.loads(s=obj, cls=extended_decoder)
    except json.JSONDecodeError:
        raise json.JSONDecodeError
    else:
        return result


def read(obj_location, extended_decoder=None):
    try:
        result = decode(sf.read_all(obj_location), extended_decoder)
    except Exception as ex:
        raise ex
    else:
        return result


def write(obj, obj_location, extended_encoder=None):
    sf.write(encode(obj, extended_encoder), obj_location)


def append(obj, obj_location, extended_encoder=None):
    raise NotImplementedError
