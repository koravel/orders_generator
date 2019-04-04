from service.database.CRUD import CRUD
from service.database.mysql.MySQLService import MySQLService


class OrderMySQLService(MySQLService, CRUD):
    __separator = ','

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

        super().execute_query(query)

    def update(self, location, params, conditions):
        set_text = ""

        for k, v in params:
            set_text += "{}={}".format(k, v)

        super().execute_query("update {} set {} where {};".format(location, set_text, conditions))

    def delete(self, location, conditions):
        super().execute_query("delete from {} where {};".format(location, conditions))

    def select(self, location, params, conditions):

        super().execute_query("select {} from {} where {};".format(location, params, conditions))
