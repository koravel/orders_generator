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

        self.__connection.try_open()

    def execute_query(self, query, params=None):
        try:
            if self.__connection.is_connected():

                connector = self.__connection.get_instance()

                cursor = connector.cursor()

                cursor.execute(query)

                connector.commit()

                cursor.close()

                if not self.__keep_connection_open:
                    connector.close()
        except Exception as ex:
            self._logger.log_error("{} occupied while executing query:\n{}".format(str(ex), query))
