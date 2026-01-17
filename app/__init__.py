from flask import Flask
from config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    from app.auth import auth
    from app.students import students

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(students, url_prefix="/students")

    return app
