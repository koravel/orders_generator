import abc
import util.TextConstants as tconst


class Provider:
    @staticmethod
    @abc.abstractmethod
    def load(location, default_location, read_method, logger):
        raise NotImplementedError(tconst.not_implemented_text.format("load"))

    @staticmethod
    @abc.abstractmethod
    def save(location, write_method, logger):
        raise NotImplementedError(tconst.not_implemented_text.format("save"))
