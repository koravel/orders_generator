import generator.basic as genbase
from generator.basic.Generator import Generator


class BigFloatGenerator(Generator):
    def get_sequence(self, min, max, length, x, y, a, c, m, t0):
        """
        Generates sequence of float numbers.
        :param min: range of numbers
        :param max: range of numbers
        :param length: length of sequence
        x, y, a, c, m, t0 - generator params, more details in /generator.basic
        """
        if min >= max:
            raise IndexError

        sequence_debug_id = "[{}{}{}{}{}{}{}{}{}]".format(length, min, max, x, y, a, c, m, t0)
        self._logger.log_trace("Generating sequence of BigFloats:{}".format(sequence_debug_id))
        try:
            for i in genbase.get_adv_sequence(x, y, a, c, m, t0, length):
                i = self._gen_next_number(i, min, max)
                self._logger.log_trace("[BigFloat]{}:{}".format(sequence_debug_id, i))
                yield i
            self._logger.log_trace("Sequence of Bins:{} was generated".format(sequence_debug_id))
        except Exception as ex:
            raise ex

    @staticmethod
    def _gen_next_number(i, min, max):
        i = genbase.check_modulo_one(i, min)
        i = genbase.check_modulo_one(i, max)

        i = genbase.check_range_modulo_zero(i, min)
        i = genbase.check_range_modulo_zero(i, max)

        i = genbase.range_zero_check(i, min, max)

        i = genbase.check_min_range(i, min)
        i = genbase.check_max_range(i, max)
        return i
