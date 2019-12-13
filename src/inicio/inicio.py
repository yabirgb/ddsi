import psycopg2 as pg

from flask import Blueprint, render_template, request

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

inicio = Blueprint('inicio', __name__, template_folder='../templates', url_prefix="/home")

@inicio.route('/', methods=['GET','POST'])
def inicio_f():

    if request.method=='GET':
        return render_template('index.html')
    else:
       
        if request.form['submit_button'] == 'Inicializar BD':
            if create_db():
                mensaje = "Ha ocurrido un error al inicializar la base de datos"
            else:
                mensaje = "Base de datos inicializada con éxito"
                
            return render_template('index.html', mensaje=mensaje)
        
        elif request.form['submit_button'] == 'Insertar datos de prueba':            
            if insert():
                mensaje = "Ha ocurrido un error al insertar los datos de prueba"
            else:
                mensaje = "Datos insertados con éxito"          
            
            return render_template('index.html', mensaje=mensaje)

        elif request.form['submit_button'] == 'Borrar datos':
            if drop_db():
                mensaje = "Ha ocurrido un error al borrar los datos"
            else:
                mensaje = "Datos eliminados con éxito"
            return render_template('index.html', mensaje=mensaje)

def create_db():
    with open('sql/creation.sql','r') as f:
        data = f.read()
        cur = conn.cursor()
        try:
            cur.execute(data)
            conn.commit()
            cur.close()
            return False
        except:
            cur.close()
            conn.rollback()
            return True

    
    with open('sql/trigger_cliente.sql','r') as f:
        data = f.read()
        cur = conn.cursor()
        try:
            cur.execute(data)
            conn.commit()
            cur.close()
            return False
        except:
            cur.close()
            conn.rollback()
            return True

def insert():
    with open('sql/insert.sql','r') as f:
        data = f.read()
        cur = conn.cursor()
        try:
            cur.execute(data)
            conn.commit()
            cur.close()
            return False
        except:
            cur.close()
            conn.rollback()
            return True
def drop_db():
    with open('sql/drop.sql','r') as f:
        data = f.read()
        cur = conn.cursor()
        try:
            cur.execute(data)
            conn.commit()
            cur.close()
            return False
        except:
            cur.close()
            conn.rollback()
            return True