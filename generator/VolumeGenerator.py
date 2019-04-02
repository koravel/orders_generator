from generator.basic.BigFloatGenerator import BigFloatGenerator


class VolumeGenerator(BigFloatGenerator):
    def get_sequence(self, length, volume_precision, x, y, a, c, m, t0, min=10, max=10000):
        """
        Generates sequence of volumes.
        :param length: length of sequence
        """
        try:
            for i in super(VolumeGenerator, self).get_sequence(
                    length=length, min=min, max=max, x=x, y=y, a=a, c=c, m=m, t0=t0):
                yield round(i, volume_precision)
        except Exception as ex:
            raise ex
