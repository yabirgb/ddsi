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
			if disponibilidad_coche(parametros[1],parametros[2],parametros[3]) == []:
				error = "Error al crear el nuevo alquiler: formato incorrecto de los datos introducidos."
			else:
				error = "En dicho periodo de alquiler el vehículo no está disponible."
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

def disponibilidad_coche(id_coche, fecha_inicio, fecha_fin):
		data = []
		consulta = "SELECT * FROM alquiler WHERE id_coche=%s and ((%s<=fecha_inicio and fecha_inicio<=%s) or (fecha_inicio<%s and %s<=fecha_fin));"
		
		if id_coche == '' or fecha_inicio == '' or fecha_fin == '':
			return data
		
		cur = conn.cursor()
		cur.execute(consulta,(id_coche,fecha_inicio,fecha_fin,fecha_inicio,fecha_inicio))
		data = cur.fetchall()
		cur.close()
		
		return data
			
@alquileres.route("/disponibilidad", methods=["GET", "POST"])
def consultar_disponibilidad():
	if request.method == 'GET':
		return render_template('disponibilidad_query.html', data=[])
    
	if request.form['submit_button'] == 'Consultar disponibilidad':
		id_coche = request.form.get("id_coche", type=str)
		fecha_inicio = request.form.get('fecha_inicio', type=str)
		fecha_fin = request.form.get('fecha_fin', type=str)
		
		if id_coche == '' or fecha_inicio == '' or fecha_fin == '':
			return render_template('disponibilidad_query.html', mensaje="No se han introducido los datos suficientes")
			
		data = disponibilidad_coche(id_coche, fecha_inicio, fecha_fin)
		
		if data == []:
			return render_template('disponibilidad_query.html', mensaje="El vehículo está disponible desde el dia " + fecha_inicio + " hasta el día " + fecha_fin)
		else:
			return render_template('disponibilidad_query.html', data=data)



@alquileres.route("/modificar_preguntar", methods=["POST"])
def modificar_alquiler_preguntar():

	dni_antiguo = request.form.get('dni_antiguo', default='')
	id_coche_antiguo = request.form.get('id_coche_antiguo', default='')
	fecha_inicio_antiguo = request.form.get('fecha_inicio_antiguo', default='')
	fecha_fin_antiguo = request.form.get('fecha_fin_antiguo', default='')
	precio_antiguo = request.form.get('precio_antiguo', default='')
	estado_antiguo = request.form.get('estado_antiguo', default='')

	return render_template('alquileres_modificar_query.html', dni_antiguo = dni_antiguo, id_coche_antiguo=id_coche_antiguo, fecha_inicio_antiguo=fecha_inicio_antiguo, fecha_fin_antiguo=fecha_fin_antiguo, precio_antiguo=precio_antiguo, estado_antiguo=estado_antiguo)

@alquileres.route("/modificar_do", methods=["POST"])
def modificar_alquiler_do():

	dni_antiguo = request.form.get('dni_antiguo', default='')
	id_coche_antiguo = request.form.get('id_coche_antiguo', default='')
	fecha_inicio_antiguo = request.form.get('fecha_inicio_antiguo', default='')
	fecha_fin_antiguo = request.form.get('fecha_fin_antiguo', default='')
	precio_antiguo = request.form.get('precio_antiguo', default='')
	estado_antiguo = request.form.get('estado_antiguo', default='')

	id_coche_nuevo = request.form.get('id_coche_nuevo', default='')
	fecha_inicio_nuevo = request.form.get('fecha_inicio_nuevo', default='')
	fecha_fin_nuevo = request.form.get('fecha_fin_nuevo', default='')
	precio_nuevo = request.form.get('precio_nuevo', default='')
	estado_nuevo = request.form.get('estado_nuevo', default='')
	
	parametros = tuple([dni_antiguo, id_coche_nuevo, fecha_inicio_nuevo, fecha_fin_nuevo, precio_nuevo, estado_nuevo, dni_antiguo, id_coche_antiguo, fecha_inicio_antiguo])
	
	cur = conn.cursor()
	query = "UPDATE alquiler SET id_coche=%s, fecha_inicio=%s, fecha_fin=%s, precio=%s, estado=%s where dni=%s and id_coche=%s and fecha_inicio=%s"
	
	try:
		cur.execute(query, ( id_coche_nuevo, fecha_inicio_nuevo, fecha_fin_nuevo, precio_nuevo, estado_nuevo, dni_antiguo, id_coche_antiguo, fecha_inicio_antiguo))
		conn.commit()
		cur.close()
		mensaje = "Datos del alquiler actualizados con éxito"
		return render_template('alquileres_modificar_query.html', mensaje = mensaje, data_new=parametros)
	except:
		cur.close()
		conn.rollback()
		if disponibilidad_coche(id_coche_nuevo, fecha_inicio_nuevo, fecha_fin_nuevo) == []:
			error = "Error: los campos introducidos no son correctos"
		else:
			error = "En dicho periodo de alquiler el vehículo no está disponible."
		return render_template('alquileres_modificar_query.html', data=[], error = error)

