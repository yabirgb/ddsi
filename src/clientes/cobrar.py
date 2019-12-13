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
        return render_template('clientes_cobrar.html', data=[])
    else:

        if request.form['submit_button'] == 'Mostrar todos':
            cur = conn.cursor()
            cur.execute("Select * from alquiler where estado='no_pagado' ")
            data = cur.fetchall()
            cur.close()


            if not data:
                mensaje = "No hay datos para mostrar."
            else:
                mensaje = ''

            return render_template('clientes_cobrar.html', data=data)
        else: 
            DNI = request.form.get('dni', default='', type=str)
            IDcoche = request.form.get('idcoche', default='', type=str)
            fechaInicio = request.form.get('fecha_inicio', default='', type=str)


            if IDcoche == '' and DNI == '' and fechaInicio == '':
                data=[]
                mensaje = "Todos los campos están vacíos, no hay datos para mostrar."            
            
            else:
                cur = conn.cursor()

                if IDcoche == '':
                    if DNI == '':
                        query = "Select * from alquiler where estado='no_pagado' and fecha_inicio=%s"
                        cur.execute(query, (fechaInicio,))
                    elif fechaInicio == '':
                        query = "Select * from alquiler where estado='no_pagado' and dni=%s"
                        cur.execute(query, (DNI,))
                    else: 
                        query = "Select * from alquiler where estado='no_pagado' and dni=%s and fecha_inicio=%s"
                        cur.execute(query, (DNI,fechaInicio))

                elif DNI == '':
                    if IDcoche == '':
                        query = "Select * from alquiler where estado='no_pagado' and fecha_inicio=%s"
                        cur.execute(query, (fechaInicio,))
                    elif fechaInicio == '':
                        query = "Select * from alquiler where estado='no_pagado' and id_coche=%s"
                        cur.execute(query, (IDcoche,))
                    else: 
                        query = "Select * from alquiler where estado='no_pagado' and id_coche=%s and fecha_inicio=%s"
                        cur.execute(query, (IDcoche,fechaInicio))

                elif fechaInicio == '':
                    if DNI == '':
                        query = "Select * from alquiler where estado='no_pagado' and id_coche=%s"
                        cur.execute(query, (IDcoche,))
                    elif IDcoche == '':
                        query = "Select * from alquiler where estado='no_pagado' and dni=%s"
                        cur.execute(query, (DNI,))
                    else: 
                        query = "Select * from alquiler where estado='no_pagado' and dni=%s and id_coche=%s"
                        cur.execute(query, (DNI,IDcoche))

                else :
                    query = "Select * from alquiler where estado='no_pagado' and DNI=%s and id_coche=%s and fecha_inicio=%s"
                    cur.execute(query,(DNI,IDcoche, fechaInicio))
                
                data = cur.fetchall()
                cur.close()

                if not data:
                    mensaje = "No hay datos para mostrar."
                else:
                    mensaje = ''
            
            return render_template('clientes_cobrar.html', data=data, mensaje=mensaje)

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
    return render_template('clientes_cobrar.html', data=[], mensaje=mensaje)
