import abc
import util.TextConstants as tconst


class DataProcessor:

    @abc.abstractmethod
    def get_result(self, data):
        raise NotImplementedError(tconst.not_implemented_text.format("get_result"))
