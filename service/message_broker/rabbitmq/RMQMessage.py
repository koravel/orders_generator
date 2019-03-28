from service.message_broker.BrokerMessage import BrokerMessage


class RMQMessage(BrokerMessage):
    def __init__(self, message, exchange, routing_key, lifetime):
        super().__init__(message, lifetime)
        self.exchange = exchange
        self.routing_key = routing_key
