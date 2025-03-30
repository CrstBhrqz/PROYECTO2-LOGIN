from app import app  # Importa tu aplicación Flask desde app.py
from asgiref.wsgi import WsgiToAsgi

# Convierte la app WSGI (Flask) a ASGI
asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    app.run(debug=False, port=5000)  # Opcional para ejecución local