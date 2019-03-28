import abc
import util.TextConstants as tconst


class DataBase:
    @abc.abstractmethod
    def execute_query(self, query, params):
        raise NotImplementedError(tconst.not_implemented_text.format("execute_query"))

