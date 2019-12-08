from flask import Flask
from flask import Blueprint, render_template, request


# from flask_api import status
from proveedores.methods import proveedores
<<<<<<< HEAD
from clientes.clientes import clientes
from clientes. cobrar import cobrar
from alquileres.methods import alquileres
=======
>>>>>>> 575b9d6035346ab79e4c904a410be63803b5483c

app = Flask(__name__)

# time.sleep(1)
app.register_blueprint(proveedores)
<<<<<<< HEAD
app.register_blueprint(clientes)
app.register_blueprint(cobrar)
app.register_blueprint(alquileres)
=======
>>>>>>> 575b9d6035346ab79e4c904a410be63803b5483c

@app.route("/")
def main2():
    return "hola"


if __name__ == "__main__":
    app.run(debug=True)
