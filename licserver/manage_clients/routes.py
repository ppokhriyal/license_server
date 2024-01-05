from flask import Blueprint, render_template, url_for, flash, request, redirect
from licserver import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from licserver.models import User, Customer
from licserver.helpers.decorators import admin_required
from licserver.manage_users.forms import EditUserForm
from sqlalchemy import func

manage_clients_route = Blueprint('manage_clients', __name__, template_folder='templates')

@manage_clients_route.route('/manage-clients', methods=['GET', 'POST'])
@login_required
def manage_clients():
    search_query = request.args.get('search_query', '').lower()
    page = request.args.get('page',1,type=int)
    # Perform a database query based on the search query
    client_query = Customer.query.filter(
        (func.lower(Customer.customer_name).ilike(f"%{search_query}%")) |
        (func.lower(Customer.customer_location).ilike(f"%{search_query}%")) |
        (func.lower(Customer.customer_email).ilike(f"%{search_query}%")) |
        (func.lower(Customer.contact_person_name).ilike(f"%{search_query}%")) |
        (func.lower(Customer.contact_email).ilike(f"%{search_query}%")) |
        (func.lower(Customer.assigned_user).ilike(f"%{search_query}%")) |
        (func.lower(Customer.contact_number).ilike(f"%{search_query}%")) 
    )
    all_clients_len = client_query.count()
    all_clients = client_query.paginate(page=page, per_page=10)
    return render_template('manage_clients/manage_client.html', title="Manage Clients", all_clients_len=all_clients_len, all_clients=all_clients, client_query=client_query )
