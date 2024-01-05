from flask import Blueprint, render_template, url_for, flash, request, redirect, session
from licserver import app, db, login_manager, bcrypt
from licserver.login.forms import LoginForm
from flask_login import login_user, current_user
from licserver.models import User

login_route = Blueprint('login', __name__, template_folder='templates')

@login_route.route('/', methods=['GET', 'POST'])
def get_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home.home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login/login.html', title='LeTOS Licensing | Login', form=form)
