import psycopg2 as pg

from flask import Blueprint, render_template, request

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

coches = Blueprint('coches', __name__,
                        template_folder='../templates', url_prefix="/coches")

@coches.route("/", methods=["GET","POST"])
def consultar_coche():

    if request.method=='GET':
        return render_template('coches_query.html', data=[])


    if request.form['submit_button'] == 'Mostrar todos':

        cur = conn.cursor()
        cur.execute("SELECT * FROM coche")
        data = cur.fetchall()
        cur.close()
        return render_template('coches_query.html', data=data)

    else:
        """consulta = "SELECT * FROM coche WHERE"
        atributos = ("id_coche","numero_bastidor","matricula","marca","modelo","color")
        parametros = []
        for i in range(6):
            aux = request.form.get(atributos[i], type=str)
            if aux != '':
                if parametros != []:
                    consulta += " and"
                parametros.append(aux)
                consulta += " " + atributos[i] + "=%s"

        parametros = tuple(parametros)


        if request.form['submit_button'] == 'Consultar coche': 

            if parametros == ():
                return render_template('coches_query.html', data=[])

            cur = conn.cursor()
            cur.execute(consulta,parametros)
            data = cur.fetchall()
            cur.close()

            return render_template('coches_query.html', data=data)
"""
        
        marca = request.form.get("marca", type=str)
        modelo = request.form.get("modelo", type=str)
        color = request.form.get("color", type=str)


        # check that all the fields are fulfilled
        if not all([marca, modelo, color]):
            msg = "Alguno de los campos no ha sido introducido correctamente"
            back = "/coches"
            return render_template("error.html", message=msg, back=back)

        # insert in the db
        sql = "INSERT INTO coche(marca, modelo, color) VALUES (%s,%s,%s)"
        
        cur = conn.cursor()
        cur.execute(sql, (marca, modelo, color))
        conn.commit()
        cur.close()
        conn.close()

        return render_template("coches_query.html", success=True)




    
@coches.route("/eliminar", methods=["POST"])
def eliminar_coche():

    cur = conn.cursor()
    cur.execute("select count(*) from cliente")
    num_tuplas = cur.fetchall()[0][0]

            
    for i in range(0,num_tuplas):
        eliminar = request.form.get(str(i), default='')
        dni = request.form.get(str(i)+'_id_coche', default='')

        if eliminar == 'on':
            cur.execute("delete from coche where id_coche=%s",(dni,))
            conn.commit()
            mensaje = "Coche(s) eliminados con éxito."
    
    cur.close()

    return render_template('coches_query.html', data=[], mensaje=mensaje)








@coches.route("/notificar_averia", methods=['GET','POST'])
def notificar_averia():
	
    id_coche = request.form.get('id_coche', default='', type=str)
    averia = request.form.get('averia', default='', type=str)

    if request.method=='GET':
        return render_template('coches_averia.html', data=[])
    if id_coche == '' or averia == '':
        msg = "Algunos de los campos está vacío"
        back = "/coches/notificar_averia"
        return render_template("error.html", message=msg, back=back)

    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT estado FROM coches WHERE id_coche=%s",
    	      (id_coche,))

        estado_previo = cur.fetchall()
        cur.close()
        if estado_previo == None:
            msg = "No se ha encontrado ningún coche con el identificador introducido"
            back = "/coches/notificar_averia"
            return render_template("error.html", message=msg, back=back)
        elif estado_previo.find(averia) == -1:
            estado_nuevo = estado_previo + averia + '/'
            cur = conn.cursor()
            cur.execute(
                "UPDATE coches SET estado = %s WHERE id_coche = %s",
    	          (estado_nuevo, id_coche))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('coches_averia.html', success=True)
        else:
            msg = "La avería introducida ya se encontraba registrada"
            back = "/coches/notificar_averia"
            return render_template("error.html", message=msg, back=back)
    except:
        cur.close()
        return render_template('coches_averia.html', errors=[])



@coches.route("/notificar_reparacion", methods=['GET','POST'])
def notificar_reparacion():
	
    id_coche = request.form.get('id_coche', default='', type=str)
    averia = request.form.get('averia', default='', type=str)

    if id_coche == '' or averia == '' or request.method=='GET':
        return render_template('coches_query.html', data=[])

    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT estado FROM coches WHERE id_coche=%s",
    	      (id_coche,))
    
        estado_previo = cur.fetchall()
        cur.close()
        if estado_previo == None:
            msg = "No se ha encontrado ningún coche con el identificador introducido"
            back = "/coches/notificar_averia"
            return render_template("error.html", message=msg, back=back)
        elif estado_previo.find(averia) != -1:
            estado_nuevo = estado_previo.replace(averia+'/', '');
            cur = conn.cursor()
            cur.execute(
                "UPDATE coches SET estado = %s WHERE id_coche = %s",
    	          (estado_nuevo, id_coche))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('coches_reparacion.html', success=True)
        else:
            msg = "La avería introducida no se encontraba registrada"
            back = "/coches/notificar_reparacion"
            return render_template("error.html", message=msg, back=back)
    except:
        cur.close()
        return render_template('coches_reparacion.html', errors=[])




@coches.route("/crear", methods=["GET", "POST"])
def crear_coche():

    if request.method == "GET":
        return render_template("coches_crear.html")
    
    marca = request.form.get("marca", type=str)
    modelo = request.form.get("modelo", type=str)
    color = request.form.get("color", type=str)


    # check that all the fields are fulfilled
    if not all([marca, modelo, color]):
        msg = "Alguno de los campos no ha sido introducido correctamente"
        back = "/coches/crear"
        return render_template("error.html", message=msg, back=back)

    # insert in the db
    sql = "INSERT INTO coche(marca, modelo, color) VALUES (%s,%s,%s)"
    
    cur = conn.cursor()
    cur.execute(sql, (marca, modelo, color))
    conn.commit()
    cur.close()
    conn.close()

    return render_template("coches_query.html", success=True)

#método matricular coche?

