import generator.basic as genbase
import generator.constants as consts
from generator.basic.BigFloatGenerator import BigFloatGenerator


class IntGenerator(BigFloatGenerator):
    def get_sequence(self, min=-consts.default_length, max=consts.default_length, length=consts.default_length,
                     x=consts.x_default, y=consts.y_default,
                     a=consts.a_default, c=consts.c_default, m=consts.m_default, t0=consts.t0_default):
        """
        Generates sequence of integer numbers.
        :param min: range of numbers
        :param max: range of numbers
        :param length: length of sequence
        x, y, a, c, m, t0 - generator params, more details in /generator.basic
        """
        if min >= max:
            raise IndexError

        element_info = "[Integer]{}:{}"
        sequence_debug_id = "[{}{}{}{}{}{}{}{}{}]".format(length, min, max, x, y, a, c, m, t0)
        self.__logger.log_trace("Generating sequence of Integers:{}".format(sequence_debug_id))
        try:
            for i in genbase.get_adv_sequence(x, y, a, c, m, t0, length):
                i = self._gen_next_number(i, min, max)
                self.__logger.log_trace(element_info.format(sequence_debug_id, i))
                yield i
            self.__logger.log_trace("Sequence of Integers:{} was generated".format(sequence_debug_id))
        except Exception as ex:
            raise ex

    @staticmethod
    def _gen_next_number(i, min, max):
        i = super()._gen_next_number(i, min, max)
        i, q = divmod(i, 1)
        i = int(i)
        return i
