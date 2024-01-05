from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from licserver.models import User

class AddNewUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    location_choices = [('Bharat', 'Bharat'),('US', 'United States'), ('London', 'London'), ('Dubai', 'Dubai')]
    user_location = SelectField('User Location', choices=location_choices)
    submit = SubmitField('Add new user')

    def validate_email(self, email):
        check_email_valid = email.data
        if not email.data.endswith('@vxlsoftware.com'):
            raise ValidationError('Please enter your valid vxlsoftware email id')
        
        user = User.query.filter_by(email=email.data).first()
        if user:
           raise ValidationError('Email id alreday added')