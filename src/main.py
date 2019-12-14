from flask import Flask
from flask import Blueprint, render_template, request, send_from_directory


# from flask_api import status
from proveedores.methods import proveedores
from clientes.clientes import clientes
from clientes.cobrar import cobrar
from alquileres.methods import alquileres
from coches.methods import coches
from inicio.inicio import inicio

app = Flask(__name__, static_url_path='')

# time.sleep(1)
app.register_blueprint(proveedores)
app.register_blueprint(clientes)
app.register_blueprint(cobrar)
app.register_blueprint(alquileres)
app.register_blueprint(coches)
app.register_blueprint(inicio)

@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)

if __name__ == "__main__":
    app.run(debug=True)
