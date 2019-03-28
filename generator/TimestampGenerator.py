import generator.basic.IntGenerator as intbase
import generator.basic.FloatGenerator as fbase
import generator.constants as consts
import config


def get_sequence(length=consts.default_length):
    """
    Generates sequence of timestamps. Adds fixed amount of second and random amount of ms.

    :param length: length of sequence
    """
    try:
        total_period_seconds = config.settings["days_amount"] * 86400
        sec_between_orders = total_period_seconds / config.settings["orders_amount"]
        period_start = config.settings["date"] - sec_between_orders
        result_timestamp = period_start

        for i in intbase.get_sequence(length=length, min=0, max=999):
            result_timestamp += sec_between_orders + i / 1000.0
            yield result_timestamp
    except Exception as ex:
        raise ex


def get_additive_sec_sequence(length=consts.default_length):
    """
    Generates sequence of  addtives to timestamps.
    :param length: length of sequence
    """
    try:
        for i in intbase.get_sequence(length=length, min=0, max=150000):
            yield i
    except Exception as ex:
        raise ex


def get_additive_ms_sequence(length=consts.default_length):
    """
    Generates sequence of  addtives to timestamps(milliseconds).
    :param length: length of sequence
    """
    try:
        for i in fbase.get_sequence(length=length, min=0):
            yield i
    except Exception as ex:
        raise ex
