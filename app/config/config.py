from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config:
    """Configuración de la aplicación."""
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///Heladeria.db')

    SQLALCHEMY_DATABASE_URI = DATABASE_URI  


    
