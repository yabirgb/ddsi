import psycopg2 as pg

from flask import Blueprint, render_template, request

conn = pg.connect(
    database='fran',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

proveedores = Blueprint('proveedores', __name__,
                        template_folder='../templates', url_prefix="/proveedores")

@proveedores.route('/consulta', methods=['GET','POST'])
def consultar_proveedores():

    #print(request.form)
    nombre = request.form.get('nombre', default='', type=str)
    CIF = request.form.get('cif', default='', type=str)

    print("data: ", nombre, CIF)

    if nombre == '' and CIF == '' or request.method=='GET':
        return render_template('proveedores_query.html', data=[])

    cur = conn.cursor()
    cur.execute(
        "Select * from proveedores where cif=%s or nombre=%s",
    	(CIF,nombre))
    
    data = cur.fetchall()


    print(data)
    cur.close()
    return render_template('proveedores_query.html', data=data)

@proveedores.route("/crear", methods=["GET", "POST"])
def crear_proveedor():

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
        back = "/proveedores/crear"
        return render_template("error.html", message=m, back=back)

    # insert in the db


    sql = "INSERT INTO proveedores(cif, nombre, ubicacion, telefono, correo) VALUES (%s,%s,%s,%s,%s)"
    
    cur = conn.cursor()
    cur.execute(sql, (nombre, ubicacion,telefono,correo,CIF))
    conn.commit()
    cur.close()
    conn.close()


@proveedores.route("/eliminar", methods=["POST"])
def eliminar_proveedor():
    pass