import config
import generators.basic.FloatGenerator as floatbase
import generators.constants as consts


def get_sequence(length=consts.default_length):
    """
    Generates sequence of price additives.
    :param length: length of sequence
    """
    try:
        for i in floatbase.get_sequence(length=length, min=-0.2, max=0.2):
            yield round(i, config.settings["price_precision"])
    except Exception as ex:
        raise ex
