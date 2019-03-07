import traceback

import mysql.connector
import config
import itertools


def default_connect():
    try:
        connection_params = config.settings["mysql"]
        return mysql.connector.connect(user=connection_params["user"], password=connection_params["password"],
                                       host=connection_params["host"], database=connection_params["database"])
    except Exception as ex:
        raise ex


def connect(connection_params):
    try:
        return mysql.connector.connect(user=connection_params["user"], password=connection_params["password"],
                                       host=connection_params["host"], database=connection_params["database"])
    except Exception as ex:
        raise ex


def close(connector):
    try:
        connector.close()
    except Exception as ex:
        raise ex


"""
def __execute(execution):
    try:
        connector = __default_connect()
    
        cursor = connector.cursor()
        
        execution()
    
        connector.commit()
    
        cursor.close()
    
        __close(connector)
    except Exception as ex:
        raise ex
"""


def execute_query(query, connector, params=[]):
    try:
        cursor = connector.cursor()
        cursor.execute(query, params)

        connector.commit()

        cursor.close()
    except Exception as ex:
        raise ex


def execute_queries(queries, connector, params=[]):
    try:
        i = 0

        cursor = connector.cursor()

        while i < len(queries):
            cursor.execute(queries[i], params[i])
            i += 1

        connector.commit()

        cursor.close()
    except Exception as ex:
        raise ex


def execute_queries_yield(queries, connector, params=()):
    try:
        cursor = connector.cursor()

        for query in queries:
            try:
                param = params.__next__()
            except:
                param = ()

            cursor.execute(query, param)

        connector.commit()

        cursor.close()
    except Exception as ex:
        raise ex


def execute_query_with_diff_params(query, connector, params):
    try:
        i = 0

        cursor = connector.cursor()

        while i < len(params):
            cursor.execute(query, params[i])
            i += 1

        connector.commit()

        cursor.close()
    except Exception as ex:
        raise ex
