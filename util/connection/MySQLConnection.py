import time
import mysql.connector

from util.connection.ServiceConnection import ServiceConnection
import util.connection as uc


class MySQLConnection(ServiceConnection):
    def __init__(self, host, port, db, logger, user, password='', retry_amount=0, retry_timeout=0):
        self.__host = host
        self.__port = port,
        self.__db = db
        self.__user = user
        self.__password = password
        self.__retry_amount = retry_amount
        self.__retry_timeout = retry_timeout
        self.__logger = logger

    def open(self):
        retry_amount_left = self.__retry_amount
        retry_timeout = self.__retry_timeout
        connection_established = False

        while retry_amount_left > 0 and not connection_established:
            try:
                self.instance = mysql.connector.connect(
                    host=self.__host,
                    port=self.__port,
                    database=self.__db,
                    user=self.__user,
                    password=self.__password
                )
            except:
                retry_amount_left -= 1
                time.sleep(retry_timeout)
            connection_established = True

        retry_amount = self.__retry_amount - retry_amount_left
        retry_time = retry_amount * retry_timeout
        connection_params_text = uc.__get_connection_params_text(
            ["host", self.__host, "port", self.__port, "db", self.__db, "user", self.__user, "pwd:", self.__password])

        if connection_established:
            self.__logger.log_info(uc.__connection_result_text.format(
                "established", retry_amount, retry_time, connection_params_text))
        else:
            self.__logger.log_error(uc.__connection_result_text.format(
                "failed", retry_amount, retry_time, connection_params_text))

    def close(self):
        if self.instance is not None:
            self.instance.close()

    def is_connected(self):
            retry_amount = self.__retry_amount

            while retry_amount > 0:
                if self.instance is not None and self.instance.is_connected():
                    return True, retry_amount
                retry_amount -= 1
                time.sleep(self.__retry_timeout)
            return False, -1
