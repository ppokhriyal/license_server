from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from licserver.models import User

class EditUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    location_choices = [('Bharat', 'Bharat'),('US', 'United States'), ('London', 'London'), ('Dubai', 'Dubai')]
    user_location = SelectField('User Location', choices=location_choices)
    submit = SubmitField('Update User')