from pathlib import Path

from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage

from src.domain.detector.models import UserImage


def test_index(client: FlaskClient):
    rv = client.get("/detector/")
    assert "Login" in rv.data.decode()
    assert "Upload image" in rv.data.decode()


def signup(
    client: FlaskClient, username: str, email: str, password: str
) -> TestResponse:
    """
    Signup(Login) to test page
    :param client: Fixture flask test client
    :param username:
    :param email:
    :param password:
    :return: Login response. It may be index page(detector.index)
    """
    data = dict(username=username, email=email, password=password)
    return client.post("/user/signup", data=data, follow_redirects=True)


def test_index_signup(client: FlaskClient):
    rv = signup(client, "admin", "testtalmo@example.com", "test_password")
    assert "admin" in rv.data.decode()

    rv = client.get("/detector/")
    assert "Logout" in rv.data.decode()
    assert "Upload image" in rv.data.decode()


def test_upload_no_auth(client: FlaskClient):
    rv = client.get("/detector/upload", follow_redirects=True)
    assert "Select the image to upload" not in rv.data.decode()

    assert "Email" in rv.data.decode()
    assert "Password" in rv.data.decode()


def test_upload_auth(client: FlaskClient):
    signup(client, "admin", "testtalmo@example.com", "test_password")
    rv = client.get("/detector/upload")
    assert "Select the image to upload" in rv.data.decode()


def upload_image(client: FlaskClient, image_path):
    image = Path(get_root_path("tests"), image_path)

    test_file = FileStorage(
        stream=open(image, "rb"),
        filename=Path(image_path).name,
        content_type="multipart/form-data",
    )

    data = dict(image=test_file)
    return client.post("/detector/upload", data=data, follow_redirects=True)


def test_upload_signup_post_validate(client: FlaskClient):
    signup(client, "admin", "testtalmo@example.com", "test_password")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")

    assert "Image files only" in rv.data.decode()


def test_upload_signup_post(client: FlaskClient):
    signup(client, "admin", "testtalmo@example.com", "test_password")
    rv = upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()


def test_detect_no_user_image(client: FlaskClient):
    signup(client, "admin", "testtalmo@example.com", "test_password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")

    rv = client.post("/detector/detect/12312321312", follow_redirects=True)
    assert "Image not found" in rv.data.decode()


def test_detect(client: FlaskClient):
    signup(client, "admin", "testtalmo@example.com", "test_password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    rv = client.post(f"/detector/detect/{user_image.id}", follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()


def test_detect_search(client: FlaskClient):
    signup(client, "admin", "testtalmo@example.com", "test_password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    client.post(f"/detector/detect/{user_image.id}", follow_redirects=True)

    rv = client.get("/detector/images/search?search=dog")
    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()

    rv = client.get("/detector/images/search?search=test")
    assert user_image.image_path not in rv.data.decode()
    assert "dog" not in rv.data.decode()


def test_delete(client: FlaskClient):
    signup(client, "admin", "testtalmo@example.com", "test_password")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    image_path = user_image.image_path
    rv = client.post(f"/detector/images/delete/{user_image.id}", follow_redirects=True)
    assert image_path not in rv.data.decode()


def test_custom_error(client: FlaskClient):
    rv = client.get("/notfound")
    assert "404 Not Found" in rv.data.decode()
