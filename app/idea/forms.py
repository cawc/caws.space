from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class IdeaForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=[('none','None'), ('book','Book'), ('series','Series'), ('anime','Anime'), ('movie', 'Movie'), ('game', 'Game')], default='none')
    done = BooleanField('Done')
    submit = SubmitField('Save')
