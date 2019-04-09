from collections import deque

from service.message_broker.MessageBroker import MessageBroker
from service.message_broker.MessageBrokerQueueing import MessageBrokerQueueing
from service.message_broker.MessageBrokerRouting import MessageBrokerRouting
#from threading.TaskThread import TaskThread
from service.message_broker.rabbitmq.RMQMessage import RMQMessage


class RabbitMQService(MessageBroker, MessageBrokerQueueing, MessageBrokerRouting):
    def __init__(self, connection, logger, thread_pool=None, enable_cache=False, message_ttl=0):
        self.__connection = connection
        self.__logger = logger
        self.__connection.open()
        self.__enable_cache = enable_cache
        self.__message_ttl = message_ttl
        self.__cache = deque()
            
        if enable_cache:
            #self.__cache_thread = TaskThread("rabbitmq_caching", thread_pool, logger)
            self.__cache_thread.setup(self.__cache_task())

        self.__connection.open()
        self.__channel = self.__connection.get_instance().channel()
        
    def __cache_task(self):
        #modify to work with multiple queues
        while True:
            if not self.is_queue_full():
                rmq_message = self.__cache.popleft()
                self.send_message(rmq_message.message, rmq_message.exchange, rmq_message.routing_key)

    def is_queue_full(self, routing_key):
        pass

    def close_channel(self):
        self.__channel.close()

    def __add_message_to_cache(self, message, exchange, routing_key):
        rmq_message = RMQMessage(message, exchange, routing_key, self.__message_ttl)
        self.__cache.append(rmq_message)
        self.__logger.log_debug("|add message:'{}' with routing_key:{} to cache".format(
            rmq_message.message, rmq_message.routing_key))
        self.__logger.log_trace("|expire at {}".format(rmq_message.expired_at))

    def send_message(self, exchange, routing_key, message):
        try:
            if self.__channel.basic_publish(
                    exchange=exchange, routing_key=routing_key, body=message, mandatory=self.__enable_cache):
                self.__add_message_to_cache(message, exchange, routing_key)
        except Exception as ex:
            self.__add_message_to_cache(message, exchange, routing_key)

    def declare_queue(self, queue_name, channel_number=0):
        self.__logger.log_debug("Declaring queue with name {} ...".format(queue_name))
        return self.__channel.queue_declare(queue=queue_name)

    def bind_queue(self, queue_name, exchange_name, routing_key=None, channel_number=0):
        self.__logger.log_debug("Binding queue {} to exchange {} with routing key {} ...".format(queue_name, exchange_name,
                                                                                             routing_key))
        return self.__channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

    def unbind_queue(self, queue_name, exchange_name, routing_key=None):
        self.__logger.log_debug("Unbinding queue {} from exchange {} with routing key {} ...".format(queue_name, exchange_name,
                                                                                       routing_key))
        return self.__channel.queue_unbind(queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)

    def purge_queue(self, queue_name):
        """
        Clearing queue
        """
        try:
            self.__logger.log_debug("Purging queue {} ...".format(queue_name))
            return self.__channel.queue_purge(queue_name)
        except Exception as ex:
            self.__logger.log_error("Queue {} not purged".format(queue_name))
            raise ex

    def delete_queue(self, queue_name, if_unused=False, if_empty=False):
        """
        Delete a queue from the broker.
        :param str queue: The queue to delete
        :param bool if_unused: only delete if it's unused
        :param bool if_empty: only delete if the queue is empty
        """
        try:
            self.__logger.log_info("Deleting queue {} ...".format(queue_name))
            return self.__channel.queue_delete(queue_name, if_unused=if_unused, if_empty=if_empty)
        except Exception as ex:
            self.__logger.log_error("Queue {} not deleted".format(queue_name))
            raise ex

    def delete_router(self, exchange_name=None, if_unused=False):
        """
        Delete exchange
        :param exchange_name: exchange name
        :param if_unused:
        """
        try:
            self.__logger.log_debug("Deleting exchange {} ...".format(exchange_name))
            return self.__channel.exchange_delete(exchange_name=exchange_name, if_unused=if_unused)
        except Exception as ex:
            self.__logger.log_error("Exchange {} not deleted".format(exchange_name))
            raise ex

    def declare_router(self, exchange_name, exchange_type, passive=False, durable=True, auto_delete=False):
        self.__logger.log_debug("Declaring exchange {} with exchange type {}".format(exchange_name, exchange_type))

        return self.__channel.exchange_declare(exchange_name,
                                                                     exchange_type=exchange_type,
                                                                     passive=passive,
                                                                     durable=durable, auto_delete=auto_delete)

    def bind_router(self, destination, source, routing_key=""):
        """
        Bind exchange
        """
        self.__logger.log_debug("Bind exchange: destination:{}, source:{}, routing_key:{}".format(
            destination, source, routing_key))
        return self.__channel.exchange_bind(destination=destination, source=source, routing_key=routing_key)

    def unbind_router(self, destination, source, routing_key=""):
        """
        Unbind exchange
        """
        self.__logger.log_debug("Unbind exchange: destination:{}, source:{}, routing_key:{}".format(
            destination, source, routing_key))
        return self.__channel.exchange_unbind(destination=destination, source=source, routing_key=routing_key)

    def consume_message(self, queue_name, on_consume_callback):
        self.__channel.basic_consume(queue=queue_name, on_message_callback=on_consume_callback)

    def start_consuming(self):
        self.__channel.start_consuming()

    def stop_consuming(self):
        self.__channel.stop_consuming()
