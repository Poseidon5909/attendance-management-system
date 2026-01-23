from flask import Flask, render_template
from config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import main
    from app.auth import auth
    from app.students import students
    from app.attendance import attendance

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(students, url_prefix="/students")
    app.register_blueprint(attendance, url_prefix="/attendance")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html"), 500

    return app
