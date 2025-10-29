from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # MongoDB configuration
    # app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_db"
    # or for cloud MongoDB Atlas
    # app.config["MONGO_URI"] = "mongodb+srv://username:password@cluster.mongodb.net/flask_db"
    
    app.config["MONGO_URI"] = "mongodb+srv://admin:admin@cluster0.xvlv0ua.mongodb.net/userdb?appName=Cluster0"
    
    mongo.init_app(app)
    
    from routes import register_routes
    register_routes(app, mongo)
    
    return app