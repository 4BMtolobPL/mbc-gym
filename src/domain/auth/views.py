from flask import Blueprint, render_template

auth_views = Blueprint(
    "auth", __name__, template_folder="templates", static_folder="static"
)


@auth_views.get("/")
def index():
    return render_template("auth/index.html")
