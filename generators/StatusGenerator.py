import generators.basic.IntGenerator as intbase
import generators.constants as consts


def get_sequence(length=consts.default_length):
    """
    Generates sequence of last statuses.
    :param length: length of sequence
    """
    try:
        for i in intbase.get_sequence(length=length, min=0, max=2):
            yield consts.statuses[i + 2]
    except Exception as ex:
        raise ex
