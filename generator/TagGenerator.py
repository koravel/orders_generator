import generator.basic.IntGenerator as intbase
import generator.constant as consts


def get_sequence(length=consts.default_length):
    """
    Generates sequence of tag ids.
    :param length: length of sequence
    """
    try:
        for i in intbase.get_sequence(length=length, min=0, max=len(consts.tags)-1):
            yield i
    except Exception as ex:
        raise ex


def get_arr_sequence(length=consts.default_length):
    """
    Generates sequence of tag id's arrays.
    :param length: length of sequence
    """
    max = 15
    arg = 12.3
    try:
        for i in get_sequence(length=length):
            yield [i, max - i, (i * (max - i)) % max, round((i * arg) % max), round(arg % (i + 1))]
    except Exception as ex:
        raise ex
