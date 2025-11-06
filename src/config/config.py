import os
from pathlib import Path

from flask import Config

basedir = Path(__file__).resolve().parent.parent.parent


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_SECRET_KEY = os.environ.get("WTF_CSRF_SECRET_KEY")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WTF_CSRF_ENABLED = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
