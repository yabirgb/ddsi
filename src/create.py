import psycopg2 as pg
import time

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='pass',
    host='localhost',
    #port=5432
)

def create_db():
    with open('sql/creation.sql','r') as f:
        data = f.read()
        cur = conn.cursor()
        cur.execute(data)
        cur.close()

def insert():
    with open('sql/insert.sql','r') as f:
        data = f.read()
        cur = conn.cursor()
        cur.execute(data)
        cur.close()

create_db()
insert()

conn.close()
