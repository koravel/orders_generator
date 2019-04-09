from service.database.CRUD import CRUD
from service.database.mysql.MySQLService import MySQLService


class CRUDService(MySQLService, CRUD):
    __separator = ','

    def __init__(self, connection, keep_connection_open, logger,
                 attempts=3, delay=0.5, instant_connection_attempts=False):
        super(CRUDService, self).__init__(connection, keep_connection_open, logger)

        self.__attempts = attempts
        self.__delay = delay
        self.__instant_connection_attempts = instant_connection_attempts

    def insert(self, location, params):
        """
        :param location: Order table
        :param params: Dictionary<field, value>
        :return:
        """
        fields = ""
        values = ""
        for k, v in params.items():
            fields += "{},".format(k)
            if isinstance(v, str):
                values += '\'{}\','.format(v)
            else:
                values += "{},".format(v)

        query = "insert into {} ({}) values({});".format(location, fields[:-1], values[:-1])

        super().execute_query(query=query, delay=self.__delay, attempts=self.__attempts,
                              instant_connection_attempts=self.__instant_connection_attempts)

    def update(self, location, params, conditions):
        set_text = ""

        for k, v in params:
            set_text += "{}={}".format(k, v)

        query = "update {} set {} where {};".format(location, set_text, conditions)

        super().execute_query(query=query, delay=self.__delay, attempts=self.__attempts,
                              instant_connection_attempts=self.__instant_connection_attempts)

    def delete(self, location, conditions):
        query = "delete from {} where {};".format(location, conditions)

        super().execute_query(query=query, delay=self.__delay, attempts=self.__attempts,
                              instant_connection_attempts=self.__instant_connection_attempts)

    def select(self, location, params, conditions):

        super().execute_query("select {} from {} where {};".format(location, params, conditions))
