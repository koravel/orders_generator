import generator.basic as genbase
from generator.basic.FloatGenerator import FloatGenerator


class IdGenerator(FloatGenerator):
    def __init__(self, logger, pow):
        super().__init__(logger)
        self.pow = pow

    def get_sequence(self, length, x, y, min=-1, max=1):
        """
        Generates sequence of ids with fixed length.
        :param pow: length of id
        :param length: length of sequence
        """
        try:
            for i in super(IdGenerator, self).get_sequence(length, x, y):
                i *= 10 ** self.pow
                i, a = divmod(i, 1)
                i = int(i)
                i = abs(i)
                i *= 10 ** (self.pow - genbase.count_digits(i))
                yield i
        except Exception as ex:
            raise ex
