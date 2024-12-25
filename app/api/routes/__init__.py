from flask import Blueprint
from app.api.routes.user import blp as user_blueprint

# You can create a parent blueprint if you want to add common functionality
api = Blueprint("api", __name__)

# List of all blueprints to register
BLUEPRINTS = [
    user_blueprint,
    # Add other blueprints here as your application grows
    # example_blueprint,
    # auth_blueprint,
]

# This function will be called from the main app factory
def init_routes(api):
    for blueprint in BLUEPRINTS:
        api.register_blueprint(blueprint, url_prefix="/api/v1")