import abc
import util.TextConstants as tconst


class DataBase:
    __instance = None

    @classmethod
    def __init__(cls):
        if cls.__instance is None:
            cls.__instance = cls

    def execute_query(self, query):
        raise NotImplementedError(tconst.not_implemented_text.format("execute_query"))

