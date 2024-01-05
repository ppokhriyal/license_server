from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# App configuration
app = Flask(__name__)
app.config["SECRET_KEY"] = "878436c0a462c4145fa59eec2c43a66a"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/license'

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
    
bcrypt = Bcrypt(app)

# Login Manager
login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login.get_login"
login_manager.login_message_category = 'info'
login_manager.needs_refresh_message = ("Session Timeout, Please login again")
login_manager.needs_refresh_message_category = "info"

# Import Blueprint routes
from licserver.login.routes import login_route
from licserver.home.routes import home_route
from licserver.add_user.routes import add_user_route
from licserver.manage_users.routes import manage_users_route
from licserver.add_client.routes import add_client_route
from licserver.manage_clients.routes import manage_clients_route

# Register Routes
app.register_blueprint(login_route)
app.register_blueprint(home_route)
app.register_blueprint(add_user_route)
app.register_blueprint(manage_users_route)
app.register_blueprint(add_client_route)
app.register_blueprint(manage_clients_route)