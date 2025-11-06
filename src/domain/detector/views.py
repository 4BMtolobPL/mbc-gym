from flask import Blueprint, render_template, send_from_directory, current_app

from src.domain.detector.models import UserImage
from src.domain.user.models import User
from src.main import db

detector_views = Blueprint(
    "detector", __name__, template_folder="templates", static_folder="static"
)


@detector_views.get("/")
def index():
    user_images = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .all()
    )

    return render_template("detector/index.html", user_images=user_images)


@detector_views.get("/images/<path:filename>")
def image_files(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
