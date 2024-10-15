import sys
sys.path.append('./Section_2')

from app import app  # Import the Flask app from the app package
from app import views  # Import the views so that the routes are recognized

if __name__ == '__main__':
    app.run(host='0.0.0.0')
