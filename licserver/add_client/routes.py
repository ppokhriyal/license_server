from flask import Blueprint, render_template, url_for, flash, request, redirect
from licserver import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required,fresh_login_required
from licserver.models import User, Customer
from licserver.add_client.forms import AddNewClientForm

add_client_route = Blueprint('add_client', __name__, template_folder='templates')

@add_client_route.route('/add-client', methods=['GET', 'POST'])
@login_required
def add_new_client():
    form = AddNewClientForm()
    if form.validate_on_submit():
        assigned_user_id = int(form.assigned_user.data)
        assigned_user_email = next((email for user_id, email in form.assigned_user.choices if user_id == assigned_user_id), None)
        client = Customer(customer_name=form.customer_name.data, customer_email=form.customer_email.data,
                          customer_address=form.customer_address.data, customer_number=form.customer_contact_number.data,
                          customer_location=form.customer_location.data, contact_person_name=form.contact_person_name.data,
                          contact_email=form.contact_person_email.data, contact_number=form.contact_person_number.data,
                          partner_name=form.partner_name.data, assigned_user=assigned_user_email, user_id=current_user.id )
        db.session.add(client)
        db.session.commit()
        flash(f"Client added successfully!", 'success')
        return redirect(url_for('home.home'))
    else:
        print(form.errors)
    return render_template('add_client/add_client.html', title="Add new client", form=form)