from flask import Flask
from flask import Blueprint, render_template, request


# from flask_api import status
from proveedores.methods import proveedores
from clientes.clientes import clientes
from clientes. cobrar import cobrar
from alquileres.methods import alquileres

app = Flask(__name__)

# time.sleep(1)
app.register_blueprint(proveedores)
app.register_blueprint(clientes)
app.register_blueprint(cobrar)
app.register_blueprint(alquileres)

@app.route("/")
def main2():
    return "hola"


if __name__ == "__main__":
    app.run(debug=True)
