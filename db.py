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

# TODO: set default date?
def init_db():
    sql_text = '''CREATE TABLE IF NOT EXISTS vocabulary (id INTEGER PRIMARY KEY AUTOINCREMENT,
    chars TEXT,
    pinyin TEXT,
    english TEXT,
    example_ch0 TEXT,
    example_eng0 TEXT,
    example_ch1 TEXT,
    example_eng1 TEXT,
    example_ch2 TEXT,
    example_eng2 TEXT,
    alpha FLOAT DEFAULT 3.0,
    beta FLOAT DEFAULT 3.0, 
    t SMALLINT DEFAULT 1,
    last DATE,
    interval SMALLINT,
    ease TINYINT,
    next DATE,
    learning BOOLEAN DEFAULT false,
    audiopath STRING,
    audioblob BLOB,
    field1,
    field2,
    field3);'''
    create_db('vocab.db', sql_text)

command = '''CREATE TABLE IF NOT EXISTS vocabulary2 (id INTEGER PRIMARY KEY AUTOINCREMENT,
    chars TEXT);'''
conn = connect('vocab.db')
conn.execute(command)