import traceback, sys

import psycopg2 as pg

from flask import Blueprint, render_template, request

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)
conn.autocommit = True


inicio = Blueprint('inicio', __name__, template_folder='../templates', url_prefix="")

@inicio.route('/', methods=['GET','POST'])
def inicio_f():

    if request.method=='GET':
        return render_template('index.html')
    else:
       
        if request.form['submit_button'] == 'Inicializar BD':
            if not create_db():
                mensaje = "Ha ocurrido un error al inicializar la base de datos"
            else:
                mensaje = "Base de datos inicializada con éxito"
            
            return render_template('index.html', mensaje='')
            #return render_template('index.html', mensaje=mensaje)
        
        elif request.form['submit_button'] == 'Insertar datos de prueba':            
            if not exec_script('sql/insert.sql'):
                mensaje = "Ha ocurrido un error al insertar los datos de prueba"
            else:
                mensaje = "Datos insertados con éxito"
                
            return render_template('index.html', mensaje=mensaje)

        elif request.form['submit_button'] == 'Borrar datos':
            if not exec_script('sql/drop.sql'):
                mensaje = "Ha ocurrido un error al borrar los datos"
            else:
                mensaje = "Datos eliminados con éxito"
            return render_template('index.html', mensaje=mensaje)

def create_db():

    resultado = exec_script('sql/creation.sql') 
    resultado = resultado and exec_script('sql/trigger_cliente.sql')
    resultado = resultado and exec_script('sql/trigger_alquiler.sql')
    resultado = resultado and exec_script('sql/trigger_coche.sql')
    resultado = resultado and exec_script('sql/trigger_proveedor.sql')

    return resultado


"""
Devuelve True si tiene éxito
"""
def exec_script(script):
    with open(script,'r') as f:
        data = f.read()
        cur = conn.cursor()
        try:
            cur.execute(data)
            conn.commit()
            cur.close()
            return True
        except:
            cur.close()
            conn.rollback()
            return False
        
