from flask import make_response, render_template
from flask_restful import Resource
from models.propietario import Propietario

class PropietarioController(Resource):
    def get(self):
        propietarios = Propietario.query.all()
        for propietario in propietarios:
            print(propietario.nombre)
        return make_response(render_template("index.html"))