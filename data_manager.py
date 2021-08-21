from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime

import database_connection


def get_secret_key():
    return database_connection.secret_key


def get_time():
    return datetime.now()


@database_connection.connection_handler
def get_user_id(cursor, username):
    query = """
    SELECT id_user
    FROM user_personal_details
    WHERE username = %(username)s
    """
    cursor.execute(query, {"username": username})
    return cursor.fetchall()


@database_connection.connection_handler
def account_exists(cursor, username, password):
    query = """
    SELECT id_user
    FROM user_personal_details
    WHERE username = %(username)s and password = %(password)s
    """
    cursor.execute(query, {"username": username, "password": password})
    return cursor.fetchall()


@database_connection.connection_handler
def register_user(cursor, username, password, registration_date, sex, age):
    query = """
    INSERT INTO user_personal_details (username,password,registration_date,sex,age)
    VALUES (%(username)s,%(password)s,%(registration_date)s,%(sex)s,%(age)s)
    """
    cursor.execute(query,
                   {"username": username, "password": password, "registration_date": registration_date, "sex": sex,
                    "age": age})


@database_connection.connection_handler
def get_all_users(cursor):
    query = """
    SELECT username,registration_date,sex,age
    FROM user_personal_details
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def post_question(cursor, question_title, question_message, id_user):
    query = """
    INSERT INTO question (title,message,submission_time,id_user)
    VALUES (%(title)s,%(message)s,%(submission_time)s,%(id_user)s)
    """
    cursor.execute(query, {"title": question_title, "message": question_message, "submission_time": get_time(),
                           "id_user": id_user},)


@database_connection.connection_handler
def get_all_questions(cursor):
    query = """
    SELECT id_question, title, message, submission_time, id_user
    FROM question
    ORDER BY id_question ASC 
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_all_questions_by_user(cursor, id_user):
    query = """
        SELECT id_question, title, message, submission_time, id_user
        FROM question
        WHERE id_user = %(id_user)s
        ORDER BY id_question ASC 
        """
    cursor.execute(query, {"id_user": id_user})
    return cursor.fetchall()
