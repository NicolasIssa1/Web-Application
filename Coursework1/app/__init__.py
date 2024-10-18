from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# I start by loading the configurations from our config.py file
app.config.from_object('config')
db = SQLAlchemy(app)

# Import views and models after creating the app and db objects to avoid circular imports
from app import views, models
