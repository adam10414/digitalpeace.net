from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class NewPostSubmissionForm(FlaskForm):
    title = StringField('Post Title: ', validators=[
        DataRequired(),
    ])

    post_body = TextAreaField('Post Body: ', validators=[DataRequired()])

    image = FileField('Image Preview: ', validators=[DataRequired()])

    image_caption = StringField('Image Captoin: ', validators=[DataRequired()])

    submit = SubmitField('Submit: ')
