import io
import psycopg2
import pandas as pd

PORT = "5432"
DB_NAME = "digitlabDB"
USER = "digitlab"
PASS = "12345678"
HOST = "localhost"


def commit_query(query_filename):
    parameters = "host={} dbname={} user={} password={} port={}".format(
        str(HOST), str(DB_NAME), str(USER), str(PASS), str(PORT)
    )
    query = ""
    with open(query_filename, "r") as fileobj:
        for row in fileobj:
            query += row.rstrip("\n")
    first_word = query[: query.find(" ")]
    connection = psycopg2.connect(parameters)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if first_word == "select" or first_word == "SELECT":
            rows = cursor.fetchall()
            print(rows)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while working with table", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def make_query(file_id, column_names, column_types):
    table_name = "dataset_{}".format(str(file_id))
    values_to_insert = []
    number_of_values = ""
    for i in range(len(column_names)):
        values_to_insert.append(column_names[i])
        values_to_insert.append(column_types[i])
    for i in range(len(values_to_insert)):
        if i == len(values_to_insert) - 1:
            number_of_values += "%s"
        elif i % 2 == 0:
            number_of_values += "%s "
        else:
            number_of_values += "%s, "
    base = "CREATE TABLE IF NOT EXISTS {}({});".format(table_name, number_of_values)
    result = base % tuple(values_to_insert)
    return result


def create_file(user_id, file_name, data_frame, column_names, column_types):
    parameters = "host={} dbname={} user={} password={} port={}".format(
        str(HOST), str(DB_NAME), str(USER), str(PASS), str(PORT)
    )
    query_for_insert = (
        "INSERT INTO USERS_FILES(user_id, file_name) VALUES(%s, %s) RETURNING file_id"
    )
    connection = psycopg2.connect(parameters)
    try:
        cursor = connection.cursor()
        cursor.execute(query_for_insert, (str(user_id), str(file_name)))
        file_id = cursor.fetchone()[0]
        query_for_create = make_query(file_id, column_names, column_types)
        cursor.execute(query_for_create)
        table_name = "dataset_{}".format(str(file_id))
        buf = io.StringIO()
        buf.write(data_frame.to_csv(index=None, header=None))
        buf.seek(0)
        with cursor as cur:
            cur.copy_from(buf, table_name, columns=column_names, sep=",")
        connection.commit()
        return file_id
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while working with database", error)
    finally:
        if connection:
            cursor.close()
            connection.close()


def get_dataframe(file_id, num_rows=None):
    parameters = "host={} dbname={} user={} password={} port={}".format(
        str(HOST), str(DB_NAME), str(USER), str(PASS), str(PORT)
    )
    table_name = "dataset_{}".format(str(file_id))
    if num_rows == None:
        query = "SELECT * FROM {}".format(table_name)
    else:
        query = "SELECT * FROM {} LIMIT {}".format(table_name, str(num_rows))
    connection = psycopg2.connect(parameters)
    try:
        df = pd.read_sql_query(query, connection)
        df.dropna(axis="index", how="any")
        connection.commit()
        return df
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating table in {}".format(DB_NAME), error)
    finally:
        if connection:
            connection.close()


def get_files(user_id):
    parameters = "host={} dbname={} user={} password={} port={}".format(
        str(HOST), str(DB_NAME), str(USER), str(PASS), str(PORT)
    )
    query = "SELECT users_files.file_id, users_files.file_name FROM USERS_FILES users_files JOIN USERS users ON users_files.user_id = users.user_id WHERE users_files.user_id = {}".format(
        str(user_id)
    )
    connection = psycopg2.connect(parameters)
    try:
        df = pd.read_sql_query(query, connection)
        df.dropna(axis="index", how="any")
        connection.commit()
        return df
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating table in {}".format(DB_NAME), error)
    finally:
        if connection:
            connection.close()
