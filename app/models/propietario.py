from config.db import db

class Propietario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), nullable= True)
    telefono = db.Column(db.String(20), nullable= True)