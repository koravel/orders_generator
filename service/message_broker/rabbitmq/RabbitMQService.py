from collections import deque

from service.message_broker.MessageBroker import MessageBroker
from service.message_broker.MessageBrokerQueueing import MessageBrokerQueueing
from service.message_broker.MessageBrokerRouting import MessageBrokerRouting
from thread.TaskThread import TaskThread
from service.message_broker.rabbitmq.RMQMessage import RMQMessage


class RabbitMQService(MessageBroker, MessageBrokerQueueing, MessageBrokerRouting):
    def __init__(self, connection, logger, thread_pool, enable_cache, cache_message_lifetime):
        self.__connection = connection
        self.__logger = logger
        self.__enable_cache = enable_cache
        self.__cache_message_lifetime = cache_message_lifetime
        self.__cache = deque()

        if enable_cache:
            self.__cache_thread = TaskThread("rabbitmq_caching", thread_pool, logger)
            self.__cache_thread.setup(self.__cache_task())

    def __cache_task(self):
        #modify to work with multiple queues
        while True:
            if not self.is_queue_full():
                rmq_message = self.__cache.popleft()
                self.send_message(rmq_message.message, rmq_message.exchange, rmq_message.routing_key)

    def send_message(self, exchange, routing_key, message):
        try:
            channel = self.__connection.channel()
            if channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message,
                                     mandatory=self.__enable_cache):
                self.__add_message_to_cache(message, exchange, routing_key)

            channel.close()
        except:
            self.__add_message_to_cache(message, exchange, routing_key)

    def __add_message_to_cache(self, message, exchange, routing_key):
        rmq_message = RMQMessage(message, exchange, routing_key, self.__cache_message_lifetime)
        self.__cache.append(rmq_message)
        self.__logger.log_debug("|add message:'{}' with routing_key:{} to cache".format(
            rmq_message.message, rmq_message.routing_key))
        self.__logger.log_trace("|expire at {}".format(rmq_message.expired_at))

    def is_queue_full(self, routing_key):
        pass

    def declare_queue(self, routing_key):
        pass

    def delete_queue(self, routing_key):
        pass

    def purge_queue(self, routing_key):
        pass

    def bind_queue(self, source, destination):
        pass

    def unbind_queue(self, source, destination):
        pass

    def declare_router(self, routing_key):
        pass

    def delete_router(self, routing_key):
        pass

    def bind_exchange(self, source, destination):
        pass

    def unbind_exchange(self, source, destination):
        pass

    def consume_message(self):
        pass