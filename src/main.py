import os

from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from src.config.config import config

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(env: str = "development"):
    app = Flask(__name__)

    if env in config:
        app.config.from_object(config[env])
    else:
        raise ValueError(f"Unknown environment: {env}")

    db.init_app(app)
    Migrate(app, db)
    csrf.init_app(app)

    from src.domain.auth import views as auth_views
    from src.domain.user import views as user_views

    app.register_blueprint(auth_views.auth_views, url_prefix="/auth")
    app.register_blueprint(user_views.user_views, url_prefix="/user")

    @app.get("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    return app
