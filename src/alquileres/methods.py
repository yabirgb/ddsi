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

    #print(request.form)
    DNI = request.form.get('DNI', default='', type=str)
    IDcoche = request.form.get('IDcoche', default='', type=str)
    fechaInicio = request.form.get('fechaInicio', default='', type=str)

    print("data: ", IDcoche, DNI, fechaInicio)

    if IDcoche == '' and DNI == '' and fechaInicio == '' or request.method=='GET':
        return render_template('alquileres_query.html', data=[])

    cur = conn.cursor()
    cur.execute(
        "Select * from alquiler where DNI=%s and id_coche=%s",
    	(DNI,IDcoche))
    
    data = cur.fetchall()


    print(data)
    cur.close()
    return render_template('alquileres_query.html', data=data)

@alquileres.route("/crear", methods=["GET", "POST"])
def crear_alquiler():

    if request.method == "GET":
        return render_template("crear_proveedor.html")
    
    nombre = request.form.get("nombre", type=str)
    ubicacion = request.form.get("ubicacion", type=str)
    telefono = request.form.get("telefono", type=int)
    correo = request.form.get("correo", type=str)
    CIF = request.form.get("cif", type=str)


    # check that all the fields are fulfilled
    if not all([nombre, ubicacion, telefono, correo, CIF]):
        m = "Alguno de los campos no ha sido introducido correctamente"
        back = "/alquiler/crear"
        return render_template("error.html", message=m, back=back)

    # insert in the db


    sql = "INSERT INTO proveedores(cif, nombre, ubicacion, telefono, correo) VALUES (%s,%s,%s,%s,%s)"
    
    cur = conn.cursor()
    cur.execute(sql, (nombre, ubicacion,telefono,correo,CIF))
    conn.commit()
    cur.close()
    conn.close()


@alquileres.route("/eliminar", methods=["POST"])
def eliminar_proveedor():
    pass
