from service.database.CRUD import CRUD
from service.database.mysql.MySQLService import MySQLService


class OrderMySQLService(MySQLService, CRUD):
    __separator = ','
    """
    Params format: Dictronary
    {
        [fields]: Array{...},
        [values]: Array{...},
        [reducers]: Array{...}
    }
    """
    def insert(self, location, params):
        fields = self.__separator.join(params["fields"])
        values = self.__separator.join(params["values"])

        super().execute_query("insert into {} ({}) values({});".format(location, fields, values))

    def update(self, location, params):

        set_text = ""
        where_text = self.__separator.join(params["reducers"])
        i = 0
        while i < len(params["fields"] / 2):
            set_text += "{}={}".format(params["fields"][i], params["values"][i])

        super().execute_query("update {} set {} where {};".format(location, set_text, where_text))

    def delete(self, location, params):
        where_text = self.__separator.join(params["reducers"])

        super().execute_query("delete from {} where {};".format(location, where_text))

    def select(self, location, params):
        fields = self.__separator.join(params["fields"])
        where_text = self.__separator.join(params["reducers"])

        super().execute_query("select {} from {} where {};".format(location, fields, where_text))
