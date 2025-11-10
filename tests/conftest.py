import os
import shutil
from typing import Generator, Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.domain.detector.models import UserImageTag, UserImage
from src.domain.user.models import User
from src.main import create_app, db


@pytest.fixture
def app_data():
    return 3


@pytest.fixture
def fixture_app() -> Generator[Flask]:
    app = create_app("testing")

    app.app_context().push()

    with app.app_context():
        db.create_all()

    os.mkdir(app.config["UPLOAD_FOLDER"])

    yield app

    User.query.delete()
    UserImage.query.delete()
    UserImageTag.query.delete()

    shutil.rmtree(app.config["UPLOAD_FOLDER"])
    db.session.commit()


@pytest.fixture
def client(fixture_app: Flask) -> FlaskClient:
    return fixture_app.test_client()
