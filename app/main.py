from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

from app.core.config import Config
from app.api.routes import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    api = Api(app)
    jwt = JWTManager(app)
    
    # Setup MongoDB with explicit database selection
    client = MongoClient(app.config["MONGODB_URI"])
    app.mongo = client.get_database(app.config["MONGODB_DB"])
    
    # Create indexes
    app.mongo.users.create_index("email", unique=True)
    
    # Register blueprints using the init_routes function
    init_routes(api)
    
    return app