from flask import Flask
from app.config.config import Config
# from app.config.db import db
from app.config.routes import register_routes

app = Flask(__name__, template_folder="views")

app.config.from_object(Config)
# db.init_app(app)
register_routes(app)

# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    app.run(debug=True)