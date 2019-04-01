import config
import generator.basic.BigFloatGenerator as bfbase
import generator.constant as consts


def get_sequence(length=consts.default_length):
    """
    Generates sequence of volumes.
    :param length: length of sequence
    """
    try:
        for i in bfbase.get_sequence(length=length, min=10, max=10000):
            yield round(i, config.settings["volume_precision"])
    except Exception as ex:
        raise ex
