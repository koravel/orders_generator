from generator.basic.IntGenerator import IntGenerator


class DescriptionGenerator(IntGenerator):
    def __init__(self, logger, descriptions_amount):
        super(DescriptionGenerator, self).__init__(logger)
        self.descriptions_amount = descriptions_amount

    def get_sequence(self, length, x, y, a, c, m, t0, min=0, max=1):
        """
        Generates sequence of description ids.
        :param length: length of sequence
        """
        try:
            for i in super(DescriptionGenerator, self).get_sequence(
                    min, self.descriptions_amount, length, x, y, a, c, m, t0):
                yield i
        except Exception as ex:
            raise ex
