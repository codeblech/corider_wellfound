from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api
from corider_flask.config import Config
from corider_flask.api.users import api as users_ns


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB
    app.mongo = PyMongo(app)

    # Initialize Flask-RESTX
    api = Api(
        app,
        version="1.0",
        title="User Management API",
        description="A simple User Management API with MongoDB",
        doc="/docs",
    )

    api.add_namespace(users_ns)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
