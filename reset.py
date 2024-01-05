from licserver import app, db, bcrypt
from licserver.models import User

with app.app_context():
    db.drop_all()
    db.create_all()

password = bcrypt.generate_password_hash('admin@123').decode('utf-8')
user = User(first_name='Prashant', last_name='Pokhriyal', email='prashant.pokhriyal@vxlsoftware.com', hashed_password=password, role='Admin', location='Bharat')

with app.app_context():
    db.session.add(user)
    db.session.commit()