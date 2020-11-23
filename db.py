import sqlite3
from sqlite3 import Error
from datetime import datetime

today = datetime.today()


def connect(filename):
    conn = None
    try:
        conn = sqlite3.connect(filename)
    except Error as e:
        print(e)
    return conn


conn = connect('vocab.db')
conn.execute('''DROP TABLE IF EXISTS vocabulary''')

conn.execute('''CREATE TABLE vocabulary
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     chars TEXT,
     pinyin TEXT,
     english TEXT,
     example_ch1 TEXT,
     example_eng1 TEXT,
     example_ch2 TEXT,
     example_eng2 TEXT,
     example_ch3 TEXT,
     example_eng3 TEXT,
     last DATE,
     ease INTEGER,
     next DATE,
     learning BOOLEAN,
     audiopath STRING,
     audioblob BLOB,
     field1,
     field2,
     field3)''')

max_cards = 100

# cursor = conn.execute('''SELECT id, chars, pinyin, english, example_ch,
# example_eng, last, ease, next, learning
#  from vocabulary
# where next <=(?)
# limit (?)''', (today.strftime("%Y=%m-%d"), str(max_cards)))


cards = [
    (
        # 'chars':
        "再见",
        # 'pinyin':
        "zàijiān",
        # 'english' :
        "Goodbye",
        # 'example_ch' =
        "就算再见...",
        # 'example_eng' =
        "Even if it's goodbye",
        # 'last':
        None,
        # 'ease':
        0,
        # 'next':
        today,
        # 'learning':
        True
    ),
    (
        # 'chars':
        "你好",
        # 'pinyin':
        "nǐhǎo",
        # 'english' :
        "Hello",
        # 'example_ch' =
        "你好，我是希卓",
        # 'example_eng' =
        "Hello I'm Theo",
        # 'last':
        None,
        # 'ease':
        0,
        # 'next':
        today,
        # 'learning':
        True
    )
        (
        # 'chars':
        "一",
        # 'pinyin':
        "yi1",
        # 'english' :
        "1",
        # 'example_ch' =
        "有一天",
        # 'example_eng' =
        "one day",
        # 'last':
        None,
        # 'ease':
        0,
        # 'next':
        today,
        # 'learning':
        True
    )
            (
        # 'chars':
        "二",
        # 'pinyin':
        "er4",
        # 'english' :
        "2",
        # 'example_ch' =
        "第二课",
        # 'example_eng' =
        "Second lesson",
        # 'last':
        None,
        # 'ease':
        0,
        # 'next':
        today,
        # 'learning':
        True
    )
               (
        # 'chars':
        "三",
        # 'pinyin':
        "san1",
        # 'english' :
        "3",
        # 'example_ch' =
        "三月",
        # 'example_eng' =
        "March",
        # 'last':
        None,
        # 'ease':
        0,
        # 'next':
        today,
        # 'learning':
        True
    )
]

conn.executemany(
    '''INSERT INTO vocabulary (chars, pinyin, english, example_ch, example_eng, last, ease, next, learning) 
    VALUES(?,?,?,?,?,?,?,?,?) ''', cards)


cursor = conn.execute('''SELECT id, chars, pinyin, english, example_ch,
example_eng, last, ease, next, learning
 from vocabulary
where next <=(?)
limit (?)''', (today.strftime("%Y=%m-%d"), str(max_cards)))
cards2 = []
for row in cursor:
    card = {
        'id': row[0],
        'chars': row[1],
        'pinyin': row[2],
        'english': row[3],
        'example_ch' : row[4],
        'example_eng' : row[5],
        'last': row[6],
        'ease': row[7],
        'next': row[8],
        'learning': row[9]
    }
    cards2.append(card)

conn.commit()
conn.close()
