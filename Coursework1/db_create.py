# Import the app and db instance from my application packages
from app import app, db

# This function is to create database tables within the app context
with app.app_context():
    db.create_all()
