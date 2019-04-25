from generator.basic.IntGenerator import IntGenerator


class LastStatusGenerator(IntGenerator):
    def get_sequence(self, length, x, y, a, c, m, t0, min=0, max=3):
        """
        Generates sequence of last statuses.
        :param length: length of sequence
        """
        try:
            for i in super(LastStatusGenerator, self).get_sequence(
                    length=length, min=min, max=max, x=x, y=y, a=a, c=c, m=m, t0=t0):
                yield i + 3
        except Exception as ex:
            raise ex
