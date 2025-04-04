from flask import Flask
from app.config.config import Config
from app.config.db import db
from app.config.routes import register_routes
from app.models.todo import Producto, Ingrediente, ProductoIngrediente
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="views")

app.config.from_object(Config)
db.init_app(app)
register_routes(app)

with app.app_context():
    print("Creando tablas")
    db.create_all()

if __name__ == "__main__":
    # Cargar variables de entorno
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 5000))  # Usa el puerto de Railway
    )