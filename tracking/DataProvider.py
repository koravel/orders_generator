import abc
import util.TextConstants as tconst


class DataProvider:
    @abc.abstractmethod
    def add_collector(self, collector):
        raise NotImplementedError(tconst.not_implemented_text.format("add_collector"))

    def remove_collector(self, collector):
        raise NotImplementedError(tconst.not_implemented_text.format("remove_collector"))
