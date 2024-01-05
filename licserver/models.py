from licserver import app, db, login_manager
from sqlalchemy.orm import backref
from flask_login import UserMixin, user_logged_out
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
    
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime(),nullable=False,default=datetime.now)
    profile_pic = db.Column(db.String(20), nullable=False, default='default_user.png')
    customers = db.relationship('Customer', backref='user', lazy=True)

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    contact_person_name = db.Column(db.String(100))
    customer_number = db.Column(db.String(15)) 
    contact_number = db.Column(db.String(15))
    partner_name = db.Column(db.String(100))
    assigned_user = db.Column(db.String(50))
    customer_email = db.Column(db.String(150), nullable=False)
    contact_email = db.Column(db.String(150), nullable=False)
    customer_address = db.Column(db.String(300), nullable=False)
    customer_location = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    license_keys = db.relationship('LicenseKeys', backref='customers_keys')


class LicenseKeys(db.Model):
    __tablename__ = "licensekeys"

    id = db.Column(db.Integer, primary_key=True)
    number_of_license_keys = db.Column(db.Integer)
    license_type = db.Column(db.String)
    allowed_devices = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

