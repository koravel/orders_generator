import abc
import util.TextConstants as tconst


class CRUD:
    @abc.abstractmethod
    def insert(self, location, params):
        raise NotImplementedError(tconst.not_implemented_text.format("insert"))

    @abc.abstractmethod
    def update(self, location, params, conditions):
        raise NotImplementedError(tconst.not_implemented_text.format("update"))

    @abc.abstractmethod
    def delete(self, location, conditions):
        raise NotImplementedError(tconst.not_implemented_text.format("delete"))

    @abc.abstractmethod
    def select(self, location, params, conditions):
        raise NotImplementedError(tconst.not_implemented_text.format("select"))
