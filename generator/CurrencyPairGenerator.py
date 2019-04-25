from generator.basic.IntGenerator import IntGenerator


class CurrencyPairGenerator(IntGenerator):
    def __init__(self, logger, currency_pairs):
        super(CurrencyPairGenerator, self).__init__(logger)
        self.currency_pairs = currency_pairs

    def get_sequence(self, length, x, y, a, c, m, t0, min=0, max=1):
        """
        Generates sequence of currency pairs.
        :param length: length of sequence
        """
        try:
            for i in super(CurrencyPairGenerator, self).get_sequence(
                    min=min, max=len(self.currency_pairs) - 1, length=length, x=x, y=y, a=a, c=c, m=m, t0=t0):
                j = 0
                for k,v in self.currency_pairs.items():
                    if j == i:
                        yield k, v
                    j += 1
        except Exception as ex:
            raise ex
