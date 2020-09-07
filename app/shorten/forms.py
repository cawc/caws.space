from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from validator_collection import is_url

from app.models import URL

def validate_url(form, field):
    if not is_url(field.data):
        raise ValidationError('Invalid URL format')

def alphanumeric(form, field):
    if not field.data.isalnum():
        raise ValidationError('Token may only contain alphanumeric characters')

def token_not_in_use(form, field):
    if URL.query.get(field.data) is not None:
        raise ValidationError(f'Token {field.data} is already in use')


class ShortenURLForm(FlaskForm):
    """Form to make a shortened url"""
    url = StringField('URL', validators=[DataRequired(), validate_url])
    token = StringField('Token', validators=[DataRequired(), alphanumeric, token_not_in_use])
    submit = SubmitField('Generate URL')
