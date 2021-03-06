import abc
import util.TextConstants as tconst


class ServiceConnection:
    @abc.abstractmethod
    def try_open(self, *args):
        raise NotImplementedError(tconst.not_implemented_text.format("try_open"))

    @abc.abstractmethod
    def open(self, *args):
        raise NotImplementedError(tconst.not_implemented_text.format("open"))

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError(tconst.not_implemented_text.format("close"))
