from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Email
from flask_wtf.file import FileAllowed,FileField
from wtforms import ValidationError

class Requirement(FlaskForm):
    name = StringField('Name ',validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    requirements = IntegerField('Food requirement (Enter number of the people for whom it is required)',validators=[DataRequired()])
    email = StringField('Enter a valid email address',validators=[DataRequired(),Email()])
    doc = FileField('User Validation Proof',validators=[FileAllowed(['jpg','png']),DataRequired()])
    contact = StringField('Contact No.',validators=[DataRequired()])
    submit = SubmitField('Submit')