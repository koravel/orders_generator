import abc
import util.TextConstants as tconst


class Generator:
    @abc.abstractmethod
    def get_sequence(self, *args, **kwargs):
        raise NotImplementedError(tconst.not_implemented_text.format("get_sequence"))
