from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///linkedin_clone.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize database and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect to login page if not logged in
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# User loader for Flask-Login
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes and models after initializing the app and db
from app import routes, models
