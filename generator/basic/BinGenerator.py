import generator.basic as genbase
import generator.constant as consts
from generator.basic.Generator import Generator


class BinGenerator(Generator):
    def __init__(self, logger):
        self.__logger = logger

    def get_sequence(self, length=consts.default_length, x=consts.x_default, y=consts.y_default):
        """
        Generates binary sequence
        :param length: length of sequence
        x, y - generator params, more details in /generator.basic
        """
        element_info = "[Bin]{}:{}"
        sequence_debug_id = "[{}{}{}]".format(length, x, y)
        self.__logger.log_trace("Generating sequence of Bins:{}".format(sequence_debug_id))
        try:
            for j in genbase.get_sequence(x, y, length):
                a, j = divmod(j, 1)
                j = abs(j)
                j = round(j)
                self.__logger.log_trace(element_info.format(sequence_debug_id, j))
                yield j
            self.__logger.log_trace("Sequence of Bins:{} was generated".format(sequence_debug_id))
        except Exception as ex:
            raise ex
