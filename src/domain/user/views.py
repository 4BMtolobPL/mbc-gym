from flask import Blueprint, render_template

from src.main import db
from src.domain.user.models import User

user_views = Blueprint(
    "user", __name__, template_folder="templates", static_folder="static"
)


@user_views.get("/")
def index():
    return render_template("user/index.html")


@user_views.get("/sql")
def sql():

    db.session.query(User).all()
    return "Check console log"
