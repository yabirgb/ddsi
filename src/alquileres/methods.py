import psycopg2 as pg

from flask import Blueprint, render_template, request

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

alquileres = Blueprint('alquileres', __name__,
                        template_folder='../templates', url_prefix="/alquileres")

@alquileres.route('/consulta', methods=['GET','POST'])
def consultar_alquileres():
	
	if request.method == 'GET':
		return render_template('alquileres_query.html', data=[])
    
	if request.form['submit_button'] == 'Consultar alquiler':
		consulta = "SELECT * FROM alquiler WHERE"
		atributos = ("dni","id_coche","fecha_inicio","fecha_fin","precio","estado")
		parametros = []

		for i in range(6):
			aux = request.form.get(atributos[i], type=str)
			if aux != '':
				if parametros != []:
					consulta += " and"
				parametros.append(aux)
				consulta += " " + atributos[i] + "=%s"

		parametros = tuple(parametros)
		
		if parametros == ():
			return render_template('alquileres_query.html', data=[])
			
		cur = conn.cursor()
		cur.execute(consulta,parametros)
		data = cur.fetchall()
		cur.close()
		
		return render_template('alquileres_query.html', data=data)
		
	elif request.form['submit_button'] == 'Crear alquiler':
		consulta = "INSERT INTO alquiler(dni,id_coche,fecha_inicio,fecha_fin,precio,estado) VALUES(%s,%s,%s,%s,%s,%s)"
		atributos = ("dni","id_coche","fecha_inicio","fecha_fin","precio","estado")
		parametros = []

		for i in range(6):
			aux = request.form.get(atributos[i], type=str)
			if aux == '':
				return render_template('alquileres_query.html', data=[])
			parametros.append(aux)

		parametros = tuple(parametros)
		
		cur = conn.cursor()
		try:
			cur.execute(consulta,parametros)
			conn.commit()
			cur.close()

			return render_template('alquileres_query.html', data_new=parametros)
		except:
			cur.close()
			conn.rollback()
			error = "Error al crear el nuevo alquiler: formato incorrecto de los datos introducidos."
			return render_template('alquileres_query.html', error=error)
		
@alquileres.route("/eliminar", methods=["POST"])
def eliminar_alquiler():

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM alquiler")
    num_tuplas = cur.fetchall()[0][0]

    msg = "No se ha eliminado ningún alquiler"
    for i in range(0,num_tuplas):
        eliminar = request.form.get(str(i), default='')
        dni = request.form.get(str(i)+'_dni', default='')
        id_coche = request.form.get(str(i)+'_id_coche', default='')
        fecha_inicio = request.form.get(str(i)+'_fecha_inicio', default='')

        if eliminar == 'on':
            cur.execute("DELETE FROM alquiler WHERE dni=%s and id_coche=%s and fecha_inicio=%s",(dni,id_coche,fecha_inicio))
            conn.commit()
            msg = "Alquiler(es) eliminado(s) con éxito."

    return render_template('alquileres_query.html', data=[], mensaje=msg)

"""
@alquileres.route("/modificar", methods=["GET", "POST"])
def modificar_alquiler():
    pass
"""

@alquileres.route("/disponibilidad", methods=["GET", "POST"])
def consultar_disponibilidad():
	if request.method == 'GET':
		return render_template('disponibilidad_query.html', data=[])
    
	if request.form['submit_button'] == 'Consultar disponibilidad':
		consulta = "SELECT * FROM alquiler WHERE id_coche=%s and ((%s<=fecha_inicio and fecha_inicio<=%s) or (fecha_inicio<%s and %s<=fecha_fin));"
		id_coche = request.form.get("id_coche", type=str)
		fecha_inicio = request.form.get('fecha_inicio', type=str)
		fecha_fin = request.form.get('fecha_fin', type=str)
		
		if id_coche == '' or fecha_inicio == '' or fecha_fin == '':
			return render_template('disponibilidad_query.html', mensaje="No se han introducido los datos suficientes")
			
		cur = conn.cursor()
		cur.execute(consulta,(id_coche,fecha_inicio,fecha_fin,fecha_inicio,fecha_inicio))
		data = cur.fetchall()
		cur.close()
		
		if data == []:
			return render_template('disponibilidad_query.html', mensaje="El vehículo está disponible desde el dia " + fecha_inicio + " hasta el día " + fecha_fin)
		else:
			return render_template('disponibilidad_query.html', data=data)

