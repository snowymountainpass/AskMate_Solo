import psycopg2
import psycopg2.extras
from decouple import config

secret_key = config('SECRET_KEY')

def get_connection_string():
    username = config('USER')
    password = config('PASSWORD')
    host = config('HOST')
    database_name = config('DATABASE')

    env_variables_defined = username and password and host and database_name

    if env_variables_defined:
        return 'postgresql://{username}:{password}@{host}/{database_name}'.format(
            username=username,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary variable(s) are not defined!')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print("Database connection problem")
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper
