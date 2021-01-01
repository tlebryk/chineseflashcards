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

def init_db():
    sql_text = '''CREATE TABLE vocabulary
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    chars TEXT,
    pinyin TEXT,
    english TEXT,
    example_ch0 TEXT,
    example_eng0 TEXT,
    example_ch1 TEXT,
    example_eng1 TEXT,
    example_ch2 TEXT,
    example_eng2 TEXT,
    interval SMALLINT,
    ease TINYINT,
    next DATE,
    learning BOOLEAN,
    audiopath STRING,
    audioblob BLOB,
    field1,
    field2,
    field3)'''
    create_db('vocab.db', sql_text)