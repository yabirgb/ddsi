import psycopg2 as pg
import time

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

def create_db():
    with open('sql/creation.sql','r') as f:
        data = f.read()
        cur = conn.cursor()
        cur.execute(data)
        cur.close()

def insert_proveedores():
    # create things
    cur = conn.cursor()
    cur.execute("INSERT INTO proveedores(cif, nombre, ubicacion, telefono, correo) VALUES (%s,%s,%s,%s,%s)", ["123456789", "FRAN", "la chana", 213122321, " fran@corre.es"])
    conn.commit()
    cur.close()

create_db()
insert_proveedores()
    
conn.close()
