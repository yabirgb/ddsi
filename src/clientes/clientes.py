import psycopg2 as pg

from flask import Blueprint, render_template, request

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

clientes = Blueprint('clientes', __name__,
                        template_folder='../templates', url_prefix="/clientes")

@clientes.route('/', methods=['GET','POST'])
def consultar_clientes():

    if request.method=='GET':
        return render_template('clientes_query_clientes.html', data=[])
    else:
       
        if request.form['submit_button'] == 'Mostrar todos':
            cur = conn.cursor()
            cur.execute("Select * from cliente ")
            
            data = cur.fetchall()

            cur.close()

            if not data:
                mensaje = "No hay datos para mostrar."
            else:
                mensaje = ''
            return render_template('clientes_query_clientes.html', data=data, mensaje=mensaje)
        
        else:
            
            dni = request.form.get('dni', default='', type=str)
            nombre = request.form.get('nombre', default='', type=str)
            telefono = request.form.get('telefono', default='', type=str)


            if request.form['submit_button'] == 'Buscar': 

                if dni == '' and nombre == '' and telefono == '':
                    data=[]
                    mensaje = "Todos los campos están vacíos, no hay datos para mostrar."
                else:
                    cur = conn.cursor()
                    cur.execute("Select * from cliente where dni=%s or nombre=%s or telefono=%s",(dni,nombre,telefono))
                    data = cur.fetchall()
                    cur.close()

                    if not data:
                        mensaje = "No hay datos para mostrar."
                    else:
                        mensaje = ''
                
                return render_template('clientes_query_clientes.html', data=data, mensaje=mensaje)


            elif request.form['submit_button'] == 'Crear nuevo':

                if dni == '' or nombre == '' or telefono == '':
                    #poner mensaje de error porque faltan campos
                    error = "Error al crear el nuevo cliente: faltan datos."
                    return render_template('clientes_query_clientes.html', data=[], error=error)
                else:
                    sql = "INSERT INTO cliente(dni, nombre, telefono) VALUES (%s,%s,%s)"
                    cur = conn.cursor()
                    cur.execute(sql, (dni, nombre, telefono))
                    conn.commit()
                    cur.close()

                    mensaje = "Nuevo cliente creado con éxito."
                    return render_template('clientes_query_clientes.html', data=[], mensaje=mensaje)
        
        


@clientes.route("/eliminar", methods=["POST"])
def eliminar_clientes():

    cur = conn.cursor()
    cur.execute("select count(*) from cliente")
    num_tuplas = cur.fetchall()[0][0]

            
    for i in range(0,num_tuplas):
        eliminar = request.form.get(str(i), default='')
        dni = request.form.get(str(i)+'_dni', default='')

        if eliminar == 'on':
            cur.execute("delete from cliente where dni=%s",(dni,))
            conn.commit()
            mensaje = "Cliente(s) eliminados con éxito."
    
    cur.close()

    return render_template('clientes_query_clientes.html', data=[], mensaje=mensaje)


@clientes.route("/consultar_alquiler", methods=["POST"])
def consultar_alquiler_cliente():

    dni = request.form.get('dni_consultar_alquiler', default='')
    mensaje = ''
    
    cur = conn.cursor()
    cur.execute("select * from alquiler where dni=%s", (dni,))
    data_alquiler = cur.fetchall()
    cur.close()

    if not data_alquiler:
        mensaje = "No hay datos para mostrar. "

    return render_template('clientes_query_alquiler.html', data=data_alquiler, mensaje=mensaje)

@clientes.route("/consultar_pendientes", methods=["POST"])
def consultar_pendientes_cliente():

    dni = request.form.get('dni_consultar_alquiler', default='')
    mensaje=''

    cur = conn.cursor()
    cur.execute("select * from alquiler where dni=%s and estado='no_pagado'", (dni,))
    data_alquiler = cur.fetchall()
    cur.close()

    if not data_alquiler:
        mensaje = "No hay datos para mostrar."

    return render_template('clientes_query_alquiler.html', data=data_alquiler, mensaje=mensaje)


@clientes.route("/modificar_preguntar", methods=["POST"])
def modificar_cliente_preguntar():

    dni_antiguo = request.form.get('dni_antiguo', default='')
    nombre_antiguo = request.form.get('nombre_antiguo', default='')
    telefono_antiguo = request.form.get('telefono_antiguo', default='')

    return render_template('clientes_query_modificar.html', dni_antiguo = dni_antiguo, nombre_antiguo=nombre_antiguo, telefono_antiguo=telefono_antiguo)

@clientes.route("/modificar_do", methods=["POST"])
def modificar_cliente_do():

    dni_antiguo = request.form.get('dni_antiguo', default='')
    nombre_antiguo = request.form.get('nombre_antiguo', default='')
    telefono_antiguo = request.form.get('telefono_antiguo', default='')

    nombre_nuevo = request.form.get('nombre_nuevo', default='')
    telefono_nuevo = request.form.get('telefono_nuevo', default='')

    cur = conn.cursor()
    query = "update cliente set nombre=%s, telefono=%s where dni=%s"
    cur.execute(query, (nombre_nuevo,telefono_nuevo, dni_antiguo))
    conn.commit()
    cur.close()    

    return render_template('clientes_query_clientes.html', data=[])

@clientes.route("/cobrar_alquiler", methods=["POST"])
def cobrar_alquiler_cliente():

    dni_cobrar = request.form.get('dni_cobrar', default='')
    idcoche_cobrar = request.form.get('idcoche_cobrar', default='')
    fecha_cobrar = request.form.get('fecha_cobrar', default='')

    cur = conn.cursor()
    query = "update alquiler set estado='pagado' where dni=%s and id_coche=%s and fecha_inicio=%s"
    cur.execute(query, (dni_cobrar, idcoche_cobrar, fecha_cobrar))
    conn.commit()
    cur.close()

    mensaje = "Cambios realizados con éxito"
    return render_template('clientes_query_alquiler.html', data=[], mensaje=mensaje)
