from generator.basic.FloatGenerator import FloatGenerator


class PriceDeviationGenerator(FloatGenerator):
    def __init__(self, logger, price_precision):
        super().__init__(logger)
        self.price_precision = price_precision

    def get_sequence(self, length, x, y, min=-0.2, max=0.2):
        """
        Generates sequence of price additives.
        :param length: length of sequence
        """
        try:
            for i in super(PriceDeviationGenerator, self).get_sequence(length=length, x=x, y=y,
                                                                                          min=-0.2, max=0.2):
                yield round(i, self.price_precision)
        except Exception as ex:
            raise ex
