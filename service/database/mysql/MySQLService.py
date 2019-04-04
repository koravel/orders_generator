from service.database.DataBase import DataBase


class MySQLService(DataBase):
    def __init__(self, connection, keep_connection_open, logger):
        """
        :param connection:
        Type of connection: MySQLConnection
        :param keep_connection_open:
        Keep connection open or open/close after each query
        """
        self.connection = connection
        self.keep_connection_open = keep_connection_open
        self.logger = logger

    def execute_query(self, query, params=None):
        try:
            if not self.connection.instance.is_connected():
                self.connection.instance.open()

            connector = self.connection.instance

            cursor = connector.cursor()

            cursor.execute(query)

            connector.commit()

            cursor.close()

            if not self.keep_connection_open:
                connector.close()
        except Exception as ex:
            self.logger.log_error("{} occupied while executing query:\n{}".format(str(ex), query), include_traceback=True)
