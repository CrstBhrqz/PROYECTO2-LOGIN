from config.db import db

class Usuario(db.Model):
    
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    @classmethod
    def check_credentials(cls, username, password):
        usuario = cls.query.filter_by(username=username).first()
        if usuario and usuario.password == password:
            return True
        return False