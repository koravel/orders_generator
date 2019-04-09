import pika

from util.connection.ServiceConnection import ServiceConnection


class RabbitMQConnection(ServiceConnection):
    def __init__(self, host, port, vhost, user, password, logger, retry_amount=1, retry_timeout=0.001):
        self.__host = host
        self.__port = port
        self.__vhost = vhost
        self.__user = user
        self.__password = password
        self.__retry_amount = retry_amount
        self.__retry_timeout = retry_timeout
        self.__logger = logger

    def open(self, *args):
        try:
            credentials = pika.PlainCredentials(self.__user, self.__password)
            self.__instance = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.__host, virtual_host=self.__vhost, credentials=credentials,
                    connection_attempts=self.__retry_amount, stack_timeout=self.__retry_timeout))
        except:
            self.__logger.log_error("RabbitMQ connection not established with params\n[{}]".format(self.__params_to_str()))
        else:
            self.__logger.log_info("RabbitMQ connection established with params\n[{}]".format(self.__params_to_str()))

    def close(self):
        if self.__instance is not None:
            self.__instance.close()

    def get_instance(self):
        return self.__instance

    def __params_to_str(self):
        return "host:{} port:{} vhost:{} user:{} password:{}".format(self.__host, self.__port, self.__vhost,
                                                                     self.__user, self.__password)
