from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_db"
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # For flash messages
    
    mongo.init_app(app)
    
    # Register routes
    from routes.person_routes import register_person_routes
    register_person_routes(app)
    
    return app