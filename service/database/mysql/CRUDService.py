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

    def insert_many(self, location, fields, values):
        """
        :param location: Order table
        :param params: Dictionary<field, value>
        """
        _fields = ""
        _values = ""
        for field in fields:
            _fields += "{},".format(field)

        for obj in values:
            value_row = ""
            for value in obj:
                if isinstance(value, str):
                    value_row += '\'{}\','.format(value)
                else:
                    value_row += "{},".format(value)
            _values += "({}),".format(value_row[:-1])

        query = "insert into {} ({}) values{};".format(location, _fields[:-1], _values[:-1])

        try:
            super().execute_query(query=query, delay=self.__delay, attempts=self.__attempts, commit=True,
                                  instant_connection_attempts=self.__instant_connection_attempts)
        except Exception as ex:
            raise ex

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
        try:
            super().execute_query(query=query, delay=self.__delay, attempts=self.__attempts,
                                  instant_connection_attempts=self.__instant_connection_attempts)
        except Exception as ex:
            raise ex

    def update(self, location, params, conditions):
        set_text = ""

        for k, v in params:
            set_text += "{}={}".format(k, v)

        query = "update {} set {} where {};".format(location, set_text, conditions)

        super().execute_query(query=query, delay=self.__delay, attempts=self.__attempts, commit=True,
                              instant_connection_attempts=self.__instant_connection_attempts)

    def delete(self, location, conditions):
        query = "delete from {} where {};".format(location, conditions)

        super().execute_query(query=query, delay=self.__delay, attempts=self.__attempts, commit=True,
                              instant_connection_attempts=self.__instant_connection_attempts)

    def select(self, params, location, conditions=None):
        query = "select {} from {}".format(params, location)
        if conditions is not None:
            query = "{} where {}".format(query, conditions)
        query += ';'

        return super().execute_query(query=query, commit=False, fetch=True, attempts=self.__attempts, delay=self.__delay,
                                     instant_connection_attempts=self.__instant_connection_attempts)
