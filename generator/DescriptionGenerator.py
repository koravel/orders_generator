import generator.basic.IntGenerator as intbase
import generator.constants as consts


def get_sequence(length=consts.default_length):
    """
    Generates sequence of description ids.
    :param length: length of sequence
    """
    try:
        for i in intbase.get_sequence(length=length, min=0, max=len(consts.descriptions) - 1):
            yield i
    except Exception as ex:
        raise ex
