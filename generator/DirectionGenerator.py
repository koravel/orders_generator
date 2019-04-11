from generator.basic.BinGenerator import BinGenerator


class DirectionGenerator(BinGenerator):
    def get_sequence(self, length, x, y):
        """
        Generates sequence of order direction ids.
        :param length: length of sequence
        """
        try:
            for i in super(DirectionGenerator, self).get_sequence(length, x, y):
                yield i + 1
        except Exception as ex:
            raise ex
