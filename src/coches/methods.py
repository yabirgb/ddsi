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

    elif request.form['submit_button'] == 'Consultar coche':
        consulta = "SELECT * FROM coche WHERE"
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

        if parametros == ():
            return render_template('coches_query.html', data=[])

        cur = conn.cursor()
        cur.execute(consulta,parametros)
        data = cur.fetchall()
        cur.close()

        return render_template('coches_query.html', data=data)





    
@coches.route("/eliminar/", methods=["POST"])
def eliminar_coche():

    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM coche")
    num_tuplas = cur.fetchall()[0][0]

    msg = "No se ha eliminado ningún coche"
    for i in range(0,num_tuplas):
        eliminar = request.form.get(str(i), default='')
        id_coche = request.form.get(str(i)+'_id_coche', default='')

        if eliminar == 'on':
            cur.execute("DELETE FROM coche WHERE id_coche=%s",(id_coche,))
            conn.commit()
            msg = "Coche(s) eliminados con éxito."
    
    cur.close()

    return render_template('coches_query.html', data=[], mensaje=msg)






@coches.route("/notificar_averia/<id_coche>/", methods=['GET','POST'])
def notificar_averia(id_coche):

    if request.method=='GET':
        return render_template('coches_averia.html', id_coche=id_coche)

    if request.form['submit_button'] == 'Guardar nueva avería':

        averia = request.form.get('averia', default='', type=str)
        if averia == '':
            msg = "No se ha introducido ninguna avería"
            back = "/coches/"
            return render_template("error.html", mensaje=msg, back=back)

        cur = conn.cursor()
        cur.execute("SELECT estado FROM coche WHERE id_coche=%s", (id_coche,))
        estado_previo = cur.fetchone()[0]
        cur.close()
        if estado_previo == None:
            estado_previo = ''

        if estado_previo.find(averia) == -1:
            estado_nuevo = estado_previo + averia + '/'
            cur = conn.cursor()
            cur.execute(
                "UPDATE coche SET estado = %s WHERE id_coche=%s",
    	          (estado_nuevo, id_coche))
            conn.commit()
            cur.close()
            msg = "La avería ha sido guardada correctamente"
            return render_template('coches_query.html', data=[], mensaje=msg)
        else:
            msg = "La avería introducida ya se encontraba registrada"
            back = "/coches/"
            return render_template("error.html", mensaje=msg, back=back)
    





@coches.route("/notificar_reparacion/<id_coche>/", methods=['GET','POST'])
def notificar_reparacion(id_coche):

    if request.method=='GET':
        return render_template('coches_reparacion.html', id_coche=id_coche)

    if request.form['submit_button'] == 'Eliminar avería':

        averia = request.form.get('averia', default='', type=str)
        if averia == '':
            msg = "No se ha introducido ninguna avería"
            back = "/coches/"
            return render_template("error.html", mensaje=msg, back=back)

        cur = conn.cursor()
        cur.execute("SELECT estado FROM coche WHERE id_coche=%s", (id_coche,))
        estado_previo = cur.fetchone()[0]
        cur.close()
        if estado_previo == None:
            estado_previo = ''

        if estado_previo.find(averia) != -1:
            estado_nuevo = estado_previo.replace(averia+'/', '');
            cur = conn.cursor()
            cur.execute(
                "UPDATE coche SET estado = %s WHERE id_coche = %s",
    	          (estado_nuevo, id_coche))
            conn.commit()
            cur.close()
            msg = "La avería ha sido eliminada correctamente"
            return render_template('coches_query.html', data=[], mensaje=msg)
        else:
            msg = "La avería introducida no se encontraba registrada"
            back = "/coches/"
            return render_template("error.html", mensaje=msg, back=back)






@coches.route("/asignar_bastidor_matricula/<id_coche>/", methods=['GET','POST'])
def asignar_bastidor_matricula(id_coche):
    if request.method=='GET':
        cur = conn.cursor()
        cur.execute(
            "SELECT numero_bastidor, matricula FROM coche WHERE id_coche = %s",
              (id_coche,))
        valores_previos = cur.fetchone()
        cur.close()
        if valores_previos == (None, None):
            return render_template('coches_bastidor_matricula.html', id_coche=id_coche)
        else:
            msg = "Este coche ya tiene un número de bastidor y una matrícula"
            back = "/coches/"
            return render_template("error.html", mensaje=msg, back=back)

    if request.form['submit_button'] == 'Asignar valores':
        numero_bastidor = request.form.get('numero_bastidor', default='', type=str)
        matricula = request.form.get('matricula', default='', type=str)
        if numero_bastidor == '' or matricula == '':
            msg = "No se ha introducido alguno de los campos requeridos"
            back = "/coches/"
            return render_template("error.html", mensaje=msg, back=back)
        else:
            cur = conn.cursor()
            cur.execute(
                    "SELECT numero_bastidor FROM coche WHERE numero_bastidor=%s",
                      (numero_bastidor,))
            bastidor_repetido = cur.fetchone()
            matricula_repetida = cur.execute(
                    "SELECT matricula FROM coche WHERE matricula=%s",
                      (matricula,))
            matricula_repetida = cur.fetchone()
            cur.close()
            if bastidor_repetido != None or matricula_repetida != None:
                conn.rollback()
                msg = "El número de bastidor o la matrícula no pueden estar ya registrados"
                back = "/coches/"
                return render_template("error.html", mensaje=msg, back=back)
            else:
                consulta = "UPDATE coche SET numero_bastidor = %s, matricula = %s WHERE id_coche = %s"
                cur = conn.cursor()
                try:
                    cur.execute(
                        "UPDATE coche SET numero_bastidor = %s, matricula = %s WHERE id_coche = %s",
                          (numero_bastidor, matricula, id_coche))
                    conn.commit()
                    cur.close()
                    msg = "Los valores han sido introducidos correctamente"
                    return render_template('coches_query.html', data=[], mensaje=msg)
                except:
                    cur.close()
                    conn.rollback()
                    msg = "Error al matricular el coche: formato incorrecto de matrícula."
                    back = "/coches/"
                    return render_template("error.html", mensaje=msg, back=back)
                





"""
@coches.route("/crear/", methods=["GET", "POST"])
def crear_coche():

    if request.method == "GET":
        return render_template("coches_crear.html")
    
    marca = request.form.get("marca", type=str)
    modelo = request.form.get("modelo", type=str)
    color = request.form.get("color", type=str)


    # check that all the fields are fulfilled
    if not all([marca, modelo, color]):
        msg = "Alguno de los campos no ha sido introducido correctamente"
        back = "/coches"
        return render_template("error.html", mensaje=msg, back=back)

    # insert in the db
    sql = "INSERT INTO coche(marca, modelo, color) VALUES (%s,%s,%s)"
        
    cur = conn.cursor()
    cur.execute(sql, (marca, modelo, color))
    conn.commit()
    cur.close()
    conn.close()

    return render_template("coches_query.html", success=True)
"""


