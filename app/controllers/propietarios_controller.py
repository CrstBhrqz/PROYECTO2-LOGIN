from flask import Blueprint, render_template
from app.models.security import Propietario

propietarios_blueprint = Blueprint("propietarios", __name__, url_prefix = "/propietarios")

@propietarios_blueprint.route("/")
def home_propietarios():
    propietarios = Propietario.query.all()
    for propietario in propietarios:
        print(propietario.nombre)
    return render_template("index.html")

@propietarios_blueprint.route("/edit")
def editar_propietarios():
    return "Este sitio funciona para editar los propietarios"