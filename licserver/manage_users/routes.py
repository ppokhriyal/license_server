from flask import Blueprint, render_template, url_for, flash, request, redirect
from licserver import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from licserver.models import User
from licserver.helpers.decorators import admin_required
from licserver.manage_users.forms import EditUserForm
from sqlalchemy import func

manage_users_route = Blueprint('manage_users', __name__, template_folder='templates')

@manage_users_route.route('/manage-users', methods=['GET', 'POST'])
@login_required
@admin_required(custom_message="You are not allowed to manage users")
def manage_users():
    search_query = request.args.get('search_query', '').lower()
    page = request.args.get('page',1,type=int)

    # Perform a database query based on the search query
    users_query = User.query.filter(
        (func.lower(User.first_name).ilike(f"%{search_query}%")) |
        (func.lower(User.last_name).ilike(f"%{search_query}%")) |
        (func.lower(User.email).ilike(f"%{search_query}%")) |
        (func.lower(User.role).ilike(f"%{search_query}%")) |
        (func.lower(User.location).ilike(f"%{search_query}%"))
    )

    all_users_len = users_query.count()
    all_users = users_query.paginate(page=page, per_page=10)
    return render_template('manage_users/manage_users.html', title="Manage Users",all_users_len=all_users_len, all_users=all_users, search_query=search_query)

# Delete user
@manage_users_route.route('/delete-user/<int:user_id>', methods=['GET','POST'])
@login_required
@admin_required(custom_message="You are not allowed to delete users")
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f"The user {user_to_delete.first_name} has been deleted", 'success' )
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting user: {str(e)}", 'danger')
    
    return redirect(url_for('manage_users.manage_users'))

# Update User
@manage_users_route.route('/update-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required(custom_message="You are not allowed to edit user information")
def update_user(user_id):
    form = EditUserForm()
    user_to_update = User.query.get_or_404(user_id)
    if form.validate_on_submit():
        user_to_update.first_name = form.first_name.data
        user_to_update.last_name = form.last_name.data
        user_to_update.location = form.user_location.data
        db.session.commit()
        flash(f"The user '{user_to_update.email}' information updated successfully", 'success')
        return redirect(url_for('manage_users.manage_users'))
    return render_template('manage_users/update_user.html', title="Update User", user_to_update=user_to_update,form=form)

