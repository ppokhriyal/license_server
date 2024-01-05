from flask import Blueprint, render_template, url_for, flash, request, redirect
from licserver import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from licserver.models import User
from licserver.add_user.forms import AddNewUserForm
from licserver.helpers.decorators import admin_required

add_user_route = Blueprint('add_user', __name__, template_folder='templates')

@add_user_route.route('/add-user', methods=['GET', 'POST'])
@login_required
@admin_required(custom_message="You are not allowed to add new user")
def add_new_user():
    form = AddNewUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data.capitalize(), last_name=form.last_name.data.capitalize(),email=form.email.data, hashed_password=hashed_password, role="Support", location=form.user_location.data)
        db.session.add(user)
        db.session.commit()
        flash(f'New user added successfully','success')
        return redirect(url_for('home.home'))
    return render_template('add_user/adduser.html', title="Add new user", form=form)