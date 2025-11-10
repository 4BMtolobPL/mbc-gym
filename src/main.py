import os

from flask import Flask, send_from_directory, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from src.config.config import config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # TODO: 미로그인 상태로 접근제한 페이지에 접속시 리다이렉트 할 엔드포인트
login_manager.login_message = ""


def create_app(env: str = "development"):
    app = Flask(__name__)

    if env in config:
        app.config.from_object(config[env])
    else:
        raise ValueError(f"Unknown environment: {env}")

    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    from src.domain.auth import views as auth_views
    from src.domain.user import views as user_views
    from src.domain.detector import views as detector_views

    app.register_blueprint(auth_views.auth_views, url_prefix="/auth")
    app.register_blueprint(user_views.user_views, url_prefix="/user")
    app.register_blueprint(detector_views.detector_views, url_prefix="/detector")

    @app.get("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app


def page_not_found(e):
    """
    404 Not Found
    :param e:
    :return:
    """
    return render_template("404.html"), 404


def internal_server_error(e):
    """
    500 Internal Server Error
    :param e:
    :return:
    """
    return render_template("500.html"), 500
