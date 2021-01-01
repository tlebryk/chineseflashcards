import sqlite3
from sqlite3 import Error
from datetime import datetime

today = datetime.today()


def connect(dbname):
    conn = None
    try:
        conn = sqlite3.connect(dbname)
    except Error as e:
        print(e)
    return conn

def create_db(dbname, sql_text):
    conn = connect(dbname)
    # delete table for testing purposes
    conn.execute('''DROP TABLE IF EXISTS vocabulary''')

    conn.execute(sql_text)

def close(conn):
    conn.commit()
    conn.close()
max_cards = 100

