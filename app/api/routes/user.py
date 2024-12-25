from flask import current_app
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.models.user import User
from app.schemas.user import UserSchema, UserLoginSchema, UserUpdateSchema
from app.core.security import verify_password, create_token

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        """Get all users"""
        users = current_app.mongo.users.find()
        return [User.from_db(user) for user in users]

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Create a new user"""
        try:
            user = User(**user_data)
            current_app.mongo.users.insert_one(user.to_dict())
            return user
        except DuplicateKeyError:
            abort(400, message="A user with this email already exists.")

@blp.route("/users/<string:user_id>")
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        """Get a user by ID"""
        user = current_app.mongo.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            abort(404, message="User not found.")
        return User.from_db(user)

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    @jwt_required()
    def put(self, user_data, user_id):
        """Update a user"""
        if get_jwt_identity() != user_id:
            abort(403, message="Not authorized to update this user.")
            
        result = current_app.mongo.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": user_data}
        )
        if result.modified_count == 0:
            abort(404, message="User not found.")
            
        user = current_app.mongo.users.find_one({"_id": ObjectId(user_id)})
        return User.from_db(user)

    @jwt_required()
    def delete(self, user_id):
        """Delete a user"""
        if get_jwt_identity() != user_id:
            abort(403, message="Not authorized to delete this user.")
            
        result = current_app.mongo.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            abort(404, message="User not found.")
        return "", 204

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, login_data):
        """Login a user"""
        user = current_app.mongo.users.find_one({"email": login_data["email"]})
        if not user or not verify_password(login_data["password"], user["password"]):
            abort(401, message="Invalid credentials.")
        
        access_token = create_token(str(user["_id"]))
        return {"access_token": access_token}