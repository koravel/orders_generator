from generator.basic.IntGenerator import IntGenerator


class LastStatusGenerator(IntGenerator):
    def get_sequence(self, statuses, length, x, y, a, c, m, t0, min=0, max=2):
        """
        Generates sequence of last statuses.
        :param length: length of sequence
        """
        try:
            for i in super(LastStatusGenerator, self).get_sequence(
                    length=length, min=min, max=max, x=x, y=y, a=a, c=c, m=m, t0=t0):
                yield statuses[i + 2]
        except Exception as ex:
            raise ex
