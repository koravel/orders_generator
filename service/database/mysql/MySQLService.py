import traceback

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

    def execute_query_with_params(self, query, params=[]):
        try:
            if self.keep_connection_open:
                if not self.connection.instance.is_connected():
                    self.connection.instance.open()
            else:
                self.connection.instance.open()

            connection = self.connection.instance

            cursor = connection.cursor()

            cursor.execute(query, params)

            connection.commit()

            cursor.close()
        except:
            self.logger.log_error(traceback.format_exc())

    def execute_query(self, query):
        try:
            if self.keep_connection_open:
                if not self.connection.instance.is_connected():
                    self.connection.instance.open()
            else:
                self.connection.instance.open()

            connection = self.connection.instance

            cursor = connection.cursor()

            cursor.execute(query)

            connection.commit()

            cursor.close()
        except:
            self.logger.log_error(traceback.format_exc())
