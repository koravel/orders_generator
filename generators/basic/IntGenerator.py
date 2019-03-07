import generators.basic as genbase
import generators.constants as consts
import utils


def get_sequence(min=-consts.default_length, max=consts.default_length, length=consts.default_length,
                 x=consts.x_default, y=consts.y_default,
                 a=consts.a_default, c=consts.c_default, m=consts.m_default, t0=consts.t0_default):
    """
    Generates sequence of integer numbers.
    :param min: range of numbers
    :param max: range of numbers
    :param length: length of sequence
    x, y, a, c, m, t0 - generator params, more details in /generators.basic
    """
    if min >= max:
        raise IndexError

    element_info = "[Integer]{}:{}"
    sequence_debug_id = "[{}{}{}{}{}{}{}{}{}]".format(length, min, max, x, y, a, c, m, t0)
    utils.logger.log_trace("Generating sequence of Integers:{}".format(sequence_debug_id))
    try:
        for i in genbase.get_adv_sequence(x, y, a, c, m, t0, length):
            i = genbase.check_modulo_one(i, min)
            i = genbase.check_modulo_one(i, max)

            i = genbase.check_range_modulo_zero(i, min)
            i = genbase.check_range_modulo_zero(i, max)

            i = genbase.range_zero_check(i, min, max)

            i = genbase.check_min_range(i, min)
            i = genbase.check_max_range(i, max)

            i, q = divmod(i, 1)
            i = int(i)
            utils.logger.log_trace(element_info.format(sequence_debug_id, i))
            yield i
        utils.logger.log_trace("Sequence of Integers:{} was generated".format(sequence_debug_id))
    except Exception as ex:
        raise ex
