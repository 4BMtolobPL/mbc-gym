from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


class UploadImageForm(FlaskForm):
    image = FileField(
        validators=[
            FileRequired("Image file is required"),
            FileAllowed(["png", "jpg", "jpeg"], "Image files only"),
        ]
    )
    submit = SubmitField("Upload")


class DetectorForm(FlaskForm):
    submit = SubmitField("Detect")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
