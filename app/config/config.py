from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\Nueva carpeta (2)\\Heladeria.db'


    