import abc
import util.TextConstants as tconst


class MessageBrokerQueueing:
    @abc.abstractmethod
    def declare_queue(self, id):
        raise NotImplementedError(tconst.not_implemented_text.format("declare_queue"))

    @abc.abstractmethod
    def delete_queue(self, id):
        raise NotImplementedError(tconst.not_implemented_text.format("delete_queue"))

    @abc.abstractmethod
    def purge_queue(self, id):
        raise NotImplementedError(tconst.not_implemented_text.format("purge_queue"))

    @abc.abstractmethod
    def bind_queue(self, source, destination):
        raise NotImplementedError(tconst.not_implemented_text.format("bind_queue"))

    @abc.abstractmethod
    def unbind_queue(self, source, destination):
        raise NotImplementedError(tconst.not_implemented_text.format("unbind_queue"))

    @abc.abstractmethod
    def is_queue_full(self, routing_key):
        raise NotImplementedError(tconst.not_implemented_text.format("is_queue_full"))