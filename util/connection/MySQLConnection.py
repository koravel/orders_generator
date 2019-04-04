import time
from mysql import connector

from util.connection.ServiceConnection import ServiceConnection
import util.connection as uc


# Yes, I've already knew, that mysql-connector MySQLConnection class already has most of this functionality :)
class MySQLConnection(ServiceConnection):
    def __init__(self, host, port, db, logger, user, password=''):
        self.__host = host
        self.__port = port
        self.__db = db
        self.__user = user
        self.__password = password
        self.__logger = logger

    def get_instance(self):
        return self.__instance

    def try_open(self, attempts=3, delay=0.5):
        retry_amount_left = attempts
        connection_established = False

        while retry_amount_left > 0 and not connection_established:
            try:
                self.open()
            except:
                retry_amount_left -= 1
                time.sleep(delay)
            else:
                connection_established = True

        retry_amount = attempts - retry_amount_left
        retry_time = retry_amount * delay

        if connection_established:
            self.__logger.log_info(uc.connection_result_text.format("MySQL", "established",
                                                                    retry_amount, retry_time,
                                                                    self.__connection_params_to_str()))
            return True
        else:
            self.__logger.log_error(uc.connection_result_text.format("MySQL", "failed",
                                                                    retry_amount, retry_time,
                                                                    self.__connection_params_to_str()))
            raise Exception

    def open(self):
        try:
            if hasattr(self, "__instance"):
                self.__instance.disconnect()

            self.__instance = connector.connect(
                host=self.__host,
                port=self.__port,
                database=self.__db,
                user=self.__user,
                password=self.__password,
                auth_plugin='mysql_native_password')
        except Exception as ex:
            self.__logger.log_error(str(ex))
            raise ConnectionError("Failed to connect with params:\n[{}]".format(self.__connection_params_to_str()))

    def close(self):
        if self.__instance is not None:
            self.__instance.close()

    def __connection_params_to_str(self):
        return uc.get_connection_params_text(
            ["host", self.__host, "port", self.__port, "db", self.__db, "user", self.__user, "password",
             self.__password])

    def is_connected(self):
        try:
            return self.__instance.is_connected()
        except:
            raise ConnectionError("Connection is not opened")
