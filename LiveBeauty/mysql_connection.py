import os
import mysql.connector
from mysql.connector import Error
from configs import cfg
cfg.run()
user = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
database = os.environ.get('DB_DATABASE')
port = os.environ.get('DB_PORT')

connection = None
try:
    connection = mysql.connector.connect(user=user, password=password,
                                         host=host,
                                         database=database, port=port)
    print("MySQL Database connection successful")
except Error as err:
    print(f"Error: '{err}'")


def disconnection():
    connection.close()


def get_values(keys_insert):
    values = []
    for i in range(0, len(keys_insert)):
        values.append('%s')
    return f"({', '.join(values)})"


def get_keys_update(keys_update, keys_insert):
    dup_s = []
    for i in range(0, len(keys_insert)):
        if keys_insert[i] not in keys_update:
            dup_s.append(f'{keys_insert[i]} = VALUES({keys_insert[i]})')
    return ','.join(dup_s)


def insert_or_update(table, keys_insert, keys_update, params):
    mycursor = connection.cursor()
    query = f"INSERT INTO {table} ({', '.join(keys_insert)}) VALUES {get_values(keys_insert)} ON DUPLICATE KEY UPDATE {get_keys_update(keys_update, keys_insert)};"
    mycursor.executemany(query, params)
    connection.commit()
    print("affected rows = {}".format(mycursor.rowcount))
    
def insert(table, keys_insert, params):
    mycursor = connection.cursor()
    query = f"INSERT INTO {table} ({', '.join(keys_insert)}) VALUES {get_values(keys_insert)};"
    mycursor.executemany(query, params)
    connection.commit()
    print("affected rows = {}".format(mycursor.rowcount))


def select_normal(table, keys, where = None):
    mycursor = connection.cursor()
    query = f"SELECT {','.join(keys)} FROM {table}"
    if where is not None:
        query += f' {where}'
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult
