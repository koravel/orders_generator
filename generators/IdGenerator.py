import generators.basic.FloatGenerator as floatbase
import generators.constants as consts
import generators.basic as genbase


def get_sequence(length=consts.default_length, pow=consts.id_length):
    """
    Generates sequence of ids with fixed length.
    :param pow: length of id
    :param length: length of sequence
    """
    try:
        for i in floatbase.get_sequence(length=length):
            i *= 10**pow
            i, a = divmod(i, 1)
            i = int(i)
            i = abs(i)
            i *= 10**(pow - genbase.count_digits(i))
            yield i
    except Exception as ex:
        raise ex
