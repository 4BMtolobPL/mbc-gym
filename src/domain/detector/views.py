from flask import Blueprint, render_template

detector_views = Blueprint(
    "detector", __name__, template_folder="templates", static_folder="static"
)


@detector_views.route("/")
def index():
    return render_template("detector/index.html")
