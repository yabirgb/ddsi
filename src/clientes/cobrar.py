import psycopg2 as pg

from flask import Blueprint, render_template, request

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

cobrar = Blueprint('cobrar', __name__,
                        template_folder='../templates', url_prefix="/cobrar")


@cobrar.route("/", methods=['GET', 'POST'])
def consultar():

    if request.method=='GET':
        return render_template('cobrar.html', data=[])
    else:

        if request.form['submit_button'] == 'Mostrar todos':
            cur = conn.cursor()
            cur.execute("Select * from alquiler where estado='no_pagado' ")
            
            data = cur.fetchall()

            cur.close()

            return render_template('cobrar.html', data=data)
        else: 
            DNI = request.form.get('dni', default='', type=str)
            IDcoche = request.form.get('idcoche', default='', type=str)
            fechaInicio = request.form.get('fecha_inicio', default='', type=str)


            if IDcoche == '' and DNI == '' and fechaInicio == '':
                return render_template('cobrar.html', data=[])

            cur = conn.cursor()
            cur.execute("Select * from alquiler where estado='no_pagado' and DNI=%s and id_coche=%s and fecha_inicio=%s",(DNI,IDcoche, fechaInicio))
            
            data = cur.fetchall()
            cur.close()
        return render_template('cobrar.html', data=data)

@cobrar.route("/cobrar_alquiler", methods=["POST"])
def cobrar_alquiler():
    dni_cobrar = request.form.get('dni_cobrar', default='')
    idcoche_cobrar = request.form.get('idcoche_cobrar', default='')
    fecha_cobrar = request.form.get('fecha_cobrar', default='')

    cur = conn.cursor()
    query = "update alquiler set estado='pagado' where dni=%s and id_coche=%s and fecha_inicio=%s"
    cur.execute(query, (dni_cobrar, idcoche_cobrar, fecha_cobrar))
    conn.commit()
    cur.close()

    mensaje = "Cambios realizados con éxito"
    return render_template('cobrar.html', data=[], mensaje=mensaje)
