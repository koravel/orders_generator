import traceback
from collections import deque

import pika

from service.message_broker.MessageBroker import MessageBroker
from service.message_broker.MessageBrokerQueueing import MessageBrokerQueueing
from service.message_broker.MessageBrokerRouting import MessageBrokerRouting
from thread.TaskThread import TaskThread
from service.message_broker.rabbitmq.RMQMessage import RMQMessage


class RabbitMQService:#(MessageBroker, MessageBrokerQueueing, MessageBrokerRouting):
    def __init__(self, connection, logger, thread_pool=None, enable_cache=None, cache_message_lifetime=None):
        self.__connection = connection
        self.__logger = logger
        self.__connection.open()
        """ self.__enable_cache = enable_cache
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
                
        def is_queue_full(self, routing_key):
            pass

    def __add_message_to_cache(self, message, exchange, routing_key):
        rmq_message = RMQMessage(message, exchange, routing_key, 0)#, self.__cache_message_lifetime)
        self.__cache.append(rmq_message)
        self.__logger.log_debug("|add message:'{}' with routing_key:{} to cache".format(
            rmq_message.message, rmq_message.routing_key))
        self.__logger.log_trace("|expire at {}".format(rmq_message.expired_at))

    """

    def send_message(self, exchange, routing_key, message):
        print("exchange={}".format(exchange))
        print("routing_key={}".format(routing_key))
        print("message={}".format(message.__class__))
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            #self.__channel = self.__connection.channel()
            channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
            #if channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message):
                #mandatory=self.__enable_cache):
                #self.__add_message_to_cache(message, exchange, routing_key)

            #self.__channel.close()
        except Exception as ex:
            #self.__add_message_to_cache(message, exchange, routing_key)
            print(str(ex))
            print(traceback.format_exc())

    def declare_queue(self, queue_name):
        '''
        Declare new queue
        :param queue_name: queue name
        :return:
        '''
        self.__connection.open()
        self.__logger.log_debug('Declaring queue with name {}'.format(queue_name))
        print(self.__connection.instance)
        return self.__connection.instance.channel().queue_declare(queue=queue_name)

    def bind_queue(self, queue_name, exchange_name, routing_key=None):
        '''
        Binding queue to exchange
        :param queue_name: queue name
        :param exchange_name: exchange name
        :param routing_key: routing key
        :return:
        '''

        self.__logger.log_debug('Binding queue {} to exchange {} with routing key  {}'.format(queue_name, exchange_name,
                                                                                             routing_key))

        return self.__connection.instance.channel().queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

    def unbind_queue(self, queue_name, exchange_name, routing_key=None):
        self.__logger.log_debug('Unbinding queue {} from exchange {} with routing key  {}'.format(queue_name, exchange_name,
                                                                                       routing_key))
        return self.__connection.queue_unbind(queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)

    def purge_queue(self, queue_name):
        '''
        Clearing queue
        :param queue_name: queue name
        :return:
        '''

        self.__logger.log_debug('Purging queue {}'.format(queue_name))
        return self.__connection.queue_purge(queue_name)

    def delete_queue(self, queue_name, if_unused=False, if_empty=False):
        self.__logger.log_debug(__file__, 'Deleting queue {}'.format(queue_name))
        return self.__connection.queue_delete(queue_name, if_unused=if_unused, if_empty=if_empty)

    def delete_router(self, exchange_name=None, if_unused=False):
        '''
        Delete exchange
        :param exchange_name: exchange name
        :param if_unused:
        :return:
        '''

        self.__logger.log_debug(__file__, 'Deleting exchange {}'.format(exchange_name))
        return self.__connection.exchange_delete(exchange_name=exchange_name, if_unused=if_unused)

    def declare_router(self, exchange_name, exchange_type, passive=False, durable=True, auto_delete=False):
        self.__logger.log_debug('Declaring exchange {} with exchange type'.format(exchange_name, exchange_type))
        self.__connection.open()
        return self.__connection.instance.channel().exchange_declare(exchange_name, exchange_type='direct', passive=passive, durable=durable,
                                                  auto_delete=auto_delete)

    def bind_router(self, destination, source, routing_key=''):
        '''
        Bind exchange
        '''

        self.__logger.log_debug(__file__,
                     'Bind exchange: destination {}, sourse, routing_key'.format(destination, source, routing_key))
        return self.__connection.exchange_bind(destination=destination, source=source, routing_key=routing_key)

    def unbind_router(self, destination, source, routing_key=''):
        '''
        Unind exchange
        '''

        self.__logger.log_debug(__file__,
                     'Unbind exchange: destination {}, sourse, routing_key'.format(destination, source, routing_key))
        return self.__connection.exchange_unbind(destination=destination, source=source, routing_key=routing_key)

    def consume_message(self, queue_name, on_consume_callback):
        self.__connection.consume(queue_name=queue_name, on_consume_callback=on_consume_callback)
