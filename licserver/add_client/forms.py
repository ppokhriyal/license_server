from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from licserver.models import User
from licserver import app, db

class AddNewClientForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    customer_address = StringField('Customer Address', validators=[DataRequired()])
    customer_contact_number = StringField('Customer Contact Number', validators=[DataRequired()])
    customer_email = StringField('Customer Email', validators=[DataRequired(), Email()])
    location_choices = [('Bharat', 'Bharat'),('US', 'United States'), ('London', 'London'), ('Dubai', 'Dubai')]
    customer_location = SelectField('User Location', choices=location_choices)
    contact_person_name = StringField('Contact Person Name', validators=[DataRequired()])
    contact_person_number = StringField('Contact Person Number', validators=[DataRequired()])
    contact_person_email = StringField('Contact Person Email', validators=[DataRequired()])
    partner_name = StringField('Partner Name', validators=[DataRequired()])
    # Querying User table for assigned_user choices
    # @staticmethod
    # def get_assigned_user_choices():
    #     with app.app_context():
    #         return [(user.id, user.email) for user in User.query.all()]
    assigned_user = SelectField('Assigned User', coerce=int)
    submit = SubmitField('Add new client')

    def __init__(self, *args, **kwargs):
        super(AddNewClientForm, self).__init__(*args, **kwargs)
        # Dynamically populate assigned_user choices
        with app.app_context():
            self.assigned_user.choices = [(user.id, user.email) for user in User.query.all()]