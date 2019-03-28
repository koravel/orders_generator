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
    def bind_exchange(self, source, destination):
        raise NotImplementedError(tconst.not_implemented_text.format("bind_exchange"))

    @abc.abstractmethod
    def unbind_exchange(self, source, destination):
        raise NotImplementedError(tconst.not_implemented_text.format("unbind_exchange"))
