# Ensures this imports the 'app' instance from my package
from app import app

if __name__ == '__main__':
    # Running the flask applicatio in debug mode.
    app.run(debug=True, port=5000)
