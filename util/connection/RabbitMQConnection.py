import time
import traceback

import pika

from util.connection.ServiceConnection import ServiceConnection


class RabbitMQConnection(ServiceConnection):
    def __init__(self, host, vhost, user, password, logger, retry_amount=0, retry_timeout=0):
        self.__host = host
        #self.__port = port
        self.__vhost = vhost
        self.__user = user
        self.__password = password
        self.__retry_amount = retry_amount
        self.__retry_timeout = retry_timeout
        self.__logger = logger

    def open(self, *args):
        try:
            credentials = pika.PlainCredentials(self.__user, self.__password)
            self.instance = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.__host, virtual_host=self.__vhost, credentials=credentials))
                    #connection_attempts=self.__retry_amount, socket_timeout=self.__retry_timeout))
        except:
            self.__logger.log_error(traceback.format_exc())
        self.__logger.log_debug("RabbitMQ connection established")

    def close(self):
        if self.instance is not None:
            self.instance.close()

    def is_connected(self):
        retry_amount = self.__retry_amount

        while retry_amount > 0:
            if self.instance is not None and self.instance.is_open:
                return True, retry_amount
            retry_amount -= 1
            time.sleep(self.__retry_timeout)
        return False, -1
