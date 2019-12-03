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
