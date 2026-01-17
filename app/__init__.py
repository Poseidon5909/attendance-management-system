from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    from app.auth import auth   # <-- this imports auth/__init__.py

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
