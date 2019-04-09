from service.database.DataBase import DataBase


class MySQLService(DataBase):
    def __init__(self, connection, keep_connection_open, logger):
        """
        :param connection:
        Type of connection: MySQLConnection
        :param keep_connection_open:
        Keep connection open or open/close after each query
        """
        self.__connection = connection
        self.__keep_connection_open = keep_connection_open
        self._logger = logger

    def execute_query(self, query, params=None, attempts=3, delay=0.5, instant_connection_attempts=False):
        if self.__connection.is_connected():

            connector = self.__connection.get_instance()

            cursor = connector.cursor()

            self.__execute(connector, cursor, query)

            cursor.close()

            if not self.__keep_connection_open:
                connector.close()
        else:
            if self.__connection.get_instance() is not None:
                self._logger.log_error("MySQL connection dropped. Try to reconnect...")
            connection_opened = False
            if instant_connection_attempts:
                while not connection_opened:
                    connection_opened = self.__connection.try_open(attempts=1, delay=delay, loop=True)
            else:
                connection_opened = self.__connection.try_open(attempts=attempts, delay=delay, loop=False)

            if connection_opened:
                self.execute_query(query, params, attempts, delay)

    def __execute(self, connector, cursor, query):
        try:
            cursor.execute(query)

            connector.commit()

        except Exception as ex:
            connector.rollback()
            self._logger.log_error("{} occupied while executing query:\n{}".format(str(ex), query))
            return False
        else:
            return True
