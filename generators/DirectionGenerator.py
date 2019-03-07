import generators.basic.BinGenerator as binbase
import generators.constants as consts


def get_sequence(length=consts.default_length):
    """
    Generates sequence of order direction ids.
    :param length: length of sequence
    """
    try:
        for i in binbase.get_sequence(length=length):
            yield i
    except Exception as ex:
        raise ex
