import generator.basic as genbase
from generator.basic.Generator import Generator


class FloatGenerator(Generator):
    def get_sequence(self, length, x, y, min=-1, max=1):
        """
        Generates sequence of decimal parts.
        :param min: range of numbers
        :param max: range of numbers
        :param length: length of sequence
        x, y, a, c, m, t0 - generator params, more details in /generator.basic
        """
        if min >= max:
            raise IndexError

        element_info = "[Float]{}:{}"
        sequence_debug_id = "[{}{}{}]".format(length, x, y)
        self._logger.log_trace("Generating sequence of Floats:{}".format(sequence_debug_id))
        try:
            for i in genbase.get_sequence(x, y, length):

                integer, i = divmod(i, 1)
                if integer < 0:
                    i *= -1

                i = genbase.range_zero_check(i, min, max)
                i = genbase.check_min_range(i, min)
                i = genbase.check_max_range(i, max)

                self._logger.log_trace(element_info.format(sequence_debug_id, i))
                yield i
            self._logger.log_trace("Sequence of Floats:{} was generated".format(sequence_debug_id))
        except Exception as ex:
            raise ex
