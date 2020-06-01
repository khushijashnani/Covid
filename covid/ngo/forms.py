from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email

class register(FlaskForm):
    name = StringField('Name ')
    