import abc
import util.TextConstants as tconst


class MessageBroker:
    @abc.abstractmethod
    def send_message(self, *args, **kwargs):
        raise NotImplementedError(tconst.not_implemented_text.format("send_message"))

    @abc.abstractmethod
    def consume_message(self, *args, **kwargs):
        raise NotImplementedError(tconst.not_implemented_text.format("consume_message"))
