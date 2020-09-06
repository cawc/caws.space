from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from validator_collection import is_url

def validate_url(form, field):
    if not is_url(field.data):
        raise ValidationError("Invalid URL format")

def alphanumeric(form, field):
    if not field.data.isalnum():
        raise ValidationError("Token may only contain alphanumeric characters")


class ShortenURLForm(FlaskForm):
    """Form to make a shortened url"""
    url = StringField('URL', validators=[DataRequired(), validate_url])
    token = StringField('Token', validators=[DataRequired(), alphanumeric])
    submit = SubmitField('Generate URL')

   
