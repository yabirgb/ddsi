import psycopg2 as pg

from flask import Blueprint, render_template, request, redirect

conn = pg.connect(
    database='ddsi',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

proveedores = Blueprint('proveedores', __name__,
                        template_folder='../templates', url_prefix="/proveedores")

@proveedores.route('/consulta', methods=['GET','POST', 'DELETE'])
def consultar_proveedores():

    #print(request.form)
    nombre = request.form.get('nombre', default='', type=str)
    CIF = request.form.get('cif', default='', type=str)

    if request.method == 'DELETE':
        CIF = request.form.get('cif', type=str)
        cur = conn.cursor()
        cur.execute("DELETE FROM proveedor where CIF=%s cascade;", (CIF,))
        cur.close()

        return render_template('proveedores_query.html', data=[], deleted=f"Proveedor con {CIF} borrado correctamente")

    print("data: ", nombre, CIF)

    if nombre == '' and CIF == '' or request.method=='GET':
        return render_template('proveedores_query.html', data=[])

    cur = conn.cursor()
    try:
        cur.execute(
            "Select * from proveedor where cif=%s or nombre ILIKE %s",
    	    (CIF,nombre))
    
        data = cur.fetchall()
        cur.close()
        return render_template('proveedores_query.html', data=data)
    except:
        cur.close()
        return render_template('proveedores_query.html', errors=[])

@proveedores.route("/crear", methods=["GET", "POST"])
def crear_proveedor():

    if request.method == "GET":
        return render_template("proveedores_crear.html")
    
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


    sql = "INSERT INTO proveedor(cif, nombre, ubicacion, telefono, correo) VALUES (%s,%s,%s,%s,%s)"
    
    cur = conn.cursor()
    cur.execute(sql, (CIF, nombre, ubicacion,telefono,correo))
    conn.commit()
    cur.close()
    conn.close()

    return render_template("proveedores_crear.html", success=True)
    

@proveedores.route("/solicitar", methods=["POST", "GET"])
def solicitar():


    campos={
        'CIF': '',
        'marca': '',
        'modelo': '',
        'color': '',
        'punto_recogida': '',
        'fecha_entrega': ''
    }

    
    if request.method == "GET":
        return render_template("solicitar_query.html", campos=campos)

    

    CIF = request.form.get("CIF", type=str, default='')
    marca = request.form.get("marca", type=str, default='')
    modelo = request.form.get("modelo", type=str, default='')
    color = request.form.get("color", type=str, default='')
    punto_recogida = request.form.get("punto", type=str, default='')
    fecha_entrega = request.form.get("fecha_entrega", default='')

    campos={
        'CIF': CIF,
        'marca': marca,
        'modelo': modelo,
        'color': color,
        'punto_recogida': punto_recogida,
        'fecha_entrega': fecha_entrega
    }

    # nos aseguramos de que el proveedor existe

    cur = conn.cursor()

    cur.execute("SELECT CIF FROM proveedor where CIF=%s", (CIF,))

    query = cur.fetchone()

    if not query:
        cur.close()
        return render_template("solicitar_query.html", err="CIF introducido no se corresponde con un proveedor válido.", campos=campos)


    cur.close()
    cur = conn.cursor()
    cur.execute("INSERT INTO coche(marca, modelo, color) VALUES (%s, %s, %s) RETURNING id_coche;", (marca, modelo, color))
    t = cur.fetchone()
    print(t)
    id_coche = t[0]
    cur.execute("INSERT INTO solicitud(id_coche, fecha_entrega, punto_recogida, cif) values(%s, %s, %s, %s)", (id_coche, fecha_entrega, punto_recogida, CIF))
    conn.commit()

    cur.close()

    return render_template("solicitar_query.html", campos=campos,success=True, msg="Coche creado correctamente")

    
 
@proveedores.route("/solicitudes", methods=["POST", "GET"])
def busqueda_solicitud():
    pass
