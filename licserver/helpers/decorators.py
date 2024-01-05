from flask import redirect, flash, url_for
from functools import wraps
from flask_login import current_user

# Decorator for admin-only routes
allowed_roles = ['Admin']

def admin_required(custom_message=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.role in allowed_roles:
                return f(*args, **kwargs)
            else:
                message = custom_message or 'You are not allowed to access this page.'
                flash(message, 'info')
                return redirect(url_for('home.home'))
        return decorated_function
    return decorator