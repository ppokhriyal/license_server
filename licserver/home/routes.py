from flask import Blueprint, render_template, url_for, flash, request, redirect, session
from licserver import db
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from licserver.models import User, Customer
from sqlalchemy import func

home_route = Blueprint('home', __name__, template_folder='templates')

@home_route.route('/home', methods=['GET', 'POST'])
def home():
    total_users = len(User.query.all()) - 1
    total_clients = len(Customer.query.all())
    # Query to get the count of users for each location
    user_counts = db.session.query(User.location, func.count(User.id)).filter(User.role == 'Support').group_by(User.location).all()
    # Convert the result to a dictionary for easy access
    user_counts_dict = dict(user_counts)

    return render_template('home/home.html', title="Home", total_users=total_users, 
                           total_clients=total_clients, user_counts_dict= user_counts_dict)

@home_route.route('/logout')
def logout():
    # Log out the user by removing session variables
    session.pop('email', None)
    logout_user()
    return redirect(url_for('login.get_login'))