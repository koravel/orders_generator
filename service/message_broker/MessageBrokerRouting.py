import abc
import util.TextConstants as tconst


class MessageBrokerRouting:
    @abc.abstractmethod
    def declare_router(self, id):
        raise NotImplementedError(tconst.not_implemented_text.format("declare_router"))

    @abc.abstractmethod
    def delete_router(self, id):
        raise NotImplementedError(tconst.not_implemented_text.format("delete_router"))

    @abc.abstractmethod
    def bind_router(self, source, destination):
        raise NotImplementedError(tconst.not_implemented_text.format("bind_router"))

    @abc.abstractmethod
    def unbind_router(self, source, destination):
        raise NotImplementedError(tconst.not_implemented_text.format("unbind_router"))
