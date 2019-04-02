from generator.basic.IntGenerator import IntGenerator


class TagGenerator(IntGenerator):
    def __init__(self, logger, tags_amount):
        super(TagGenerator, self).__init__(logger)
        self.tags_amount = tags_amount

    def get_sequence(self, length, x, y, a, c, m, t0, min=0, max=1):
        """
        Generates sequence of tag ids.
        :param length: length of sequence
        """
        try:
            for i in super(TagGenerator, self).get_sequence(
                    length=length, min=min, max=self.tags_amount - 1, x=x, y=y, a=a, c=c, m=m, t0=t0):
                yield i
        except Exception as ex:
            raise ex

    def get_arr_sequence(self, length, x, y, a, c, m, t0, min=0):
        """
        Generates sequence of tag id's arrays.
        :param length: length of sequence
        """
        max = 15
        arg = 12.3
        try:
            for i in self.get_sequence(length, x, y, a, c, m, t0, min):
                yield [i, max - i, (i * (max - i)) % max, round((i * arg) % max), round(arg % (i + 1))]
        except Exception as ex:
            raise ex
