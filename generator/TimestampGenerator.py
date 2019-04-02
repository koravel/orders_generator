from generator.basic.IntGenerator import IntGenerator


class TimestampGenerator(IntGenerator):
    def __init__(self, logger, date, days_amount):
        super(TimestampGenerator, self).__init__(logger)
        self.date = date
        self.days_amount = days_amount

    def get_sequence(self, length, x, y, a, c, m, t0, min=0, max=999):
        """
        Generates sequence of timestamps. Adds fixed amount of second and random amount of ms.

        :param length: length of sequence
        """
        try:
            total_period_seconds = self.days_amount * 86400
            sec_between_orders = total_period_seconds / length
            period_start = self.date - sec_between_orders
            result_timestamp = period_start

            for i in super(TimestampGenerator, self).get_sequence(
                    length=length, x=x, y=y, a=a, c=c, m=m, t0=t0, min=min, max=max):
                result_timestamp = result_timestamp + sec_between_orders
                result_timestamp += i / 1000.0
                result_timestamp = int(result_timestamp)
                yield result_timestamp
        except Exception as ex:
            raise ex

    def get_additive_ms_sequence(self, length, x, y, a, c, m, t0):
        """
        Generates sequence of  addtives to timestamps.
        :param length: length of sequence
        """
        try:
            for i in super(TimestampGenerator, self).get_sequence(
                    length=length, x=x, y=y, a=a, c=c, m=m, t0=t0, min=0, max=150000):
                yield i
        except Exception as ex:
            raise ex
