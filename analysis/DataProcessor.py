import abc
import util.TextConstants as tconst


class DataProcessor:
    @staticmethod
    @abc.abstractmethod
    def get_result(data):
        raise NotImplementedError(tconst.not_implemented_text.format("get_result"))
