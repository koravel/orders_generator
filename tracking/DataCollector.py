import abc
import util.TextConstants as tconst


class DataCollector:
    def __init__(self):
        self.__data = dict()

    @abc.abstractmethod
    def get_data(self, key):
        raise NotImplementedError(tconst.not_implemented_text.format("get_data"))

    @abc.abstractmethod
    def add_data(self, key, object):
        raise NotImplementedError(tconst.not_implemented_text.format("add_data"))
