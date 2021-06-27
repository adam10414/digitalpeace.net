from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class NewPostSubmissionForm(FlaskForm):
    title = StringField('Post Title: ', validators=[InputRequired()])

    post_body = TextAreaField('Post Body: ', validators=[InputRequired()])

    #TODO:
    #Limit file types to images only. (Will need to list all image file types.)
    #Or figure out how to get this to work:
    #FileAllowed(images, 'Images only please.')
    #https://pythonhosted.org/Flask-WTF/form.html

    #FileRequired() produces a bug where none of the form data is captured.
    image = FileField('Image Preview: ', validators=[InputRequired()])

    image_caption = StringField('Image Caption: ',
                                validators=[InputRequired()])

    submit = SubmitField('Submit')
