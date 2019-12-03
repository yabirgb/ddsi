from flask import Flask, render_template, request
#from flask_api import status
import psycopg2 as pg
import time

app = Flask(__name__)

conn = pg.connect(
    database='fran',
    user='postgres',
    password='postgres',
    host='localhost',
    #port=5432
)

def insert_data():
    # create things
    # cur = conn.cursor()
    # cur.execute("CREATE TABLE coches(id SERIAL, data varchar);")
    # cur.execute("INSERT INTO coches(data) VALUES (%s)", ["hola fran"])
    # conn.commit()
    # cur.close()

    pass

#time.sleep(1)


@app.route('/search')
def main():
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM coches")
    rows = cur.fetchall()
    cur.close()

    template_data = {
        'rows':rows
    }
    
    return render_template('index.html', content=template_data)

@app.route('/')
def main2():
    return "hola"

@app.route('/proveedores/consulta', methods=['GET','POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
