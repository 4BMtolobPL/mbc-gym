import uuid
from pathlib import Path

from flask import (
    Blueprint,
    render_template,
    send_from_directory,
    current_app,
    redirect,
    url_for,
)
from flask_login import login_required, current_user

from src.domain.detector.forms import UploadImageForm
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


@detector_views.route("/upload", methods=["GET", "POST"])
@login_required
def upload_image():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.image.data
        ext = Path(file.filename).suffix
        # 아래처럼 werkzeug의 secure_filename을 사용해도 될듯
        # 또는 Flask-Uploads(https://pythonhosted.org/Flask-Uploads/) 고려해보기
        # image_secure_filename = secure_filename(file.filename)
        image_uuid_file_name = str(uuid.uuid4()) + ext
        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        user_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name)

        db.session.add(user_image)
        db.session.commit()

        return redirect(url_for("detector.index"))
    return render_template("detector/upload.html", form=form)
