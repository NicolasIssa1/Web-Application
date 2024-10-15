from flask import Flask

app = Flask(__name__)

# Import views after creating the app instance to avoid circular imports
from app import views
