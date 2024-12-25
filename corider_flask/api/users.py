from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from bson import ObjectId
from corider_flask.models.user import User
from corider_flask.utils.validators import validate_email_format

api = Namespace("users", description="User operations")

user_model = api.model(
    "User",
    {
        "name": fields.String(required=True, description="User name"),
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)


@api.route("/")
class UserList(Resource):
    @api.doc("list_users")
    def get(self):
        """List all users"""
        users = current_app.mongo.db.users.find()
        return [{**user, "_id": str(user["_id"])} for user in users]

    @api.doc("create_user")
    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        data = request.json

        if not validate_email_format(data["email"]):
            api.abort(400, "Invalid email format")

        if current_app.mongo.db.users.find_one({"email": data["email"]}):
            api.abort(409, "Email already exists")

        user = User(data["name"], data["email"], data["password"])
        result = current_app.mongo.db.users.insert_one(user.to_dict())

        return {"message": "User created", "id": str(result.inserted_id)}, 201


@api.route("/<id>")
@api.param("id", "The user identifier")
class UserResource(Resource):
    @api.doc("get_user")
    def get(self, id):
        """Fetch a user by ID"""
        try:
            user = current_app.mongo.db.users.find_one({"_id": ObjectId(id)})
            if user:
                user["_id"] = str(user["_id"])
                return user
            api.abort(404, "User not found")
        except Exception:
            api.abort(400, "Invalid ID format")

    @api.doc("update_user")
    @api.expect(user_model)
    def put(self, id):
        """Update a user"""
        try:
            data = request.json
            if not current_app.mongo.db.users.find_one({"_id": ObjectId(id)}):
                api.abort(404, "User not found")

            if "email" in data and not validate_email_format(data["email"]):
                api.abort(400, "Invalid email format")

            update_data = {k: v for k, v in data.items() if k != "password"}
            if "password" in data:
                update_data["password"] = User._hash_password(data["password"])

            current_app.mongo.db.users.update_one(
                {"_id": ObjectId(id)}, {"$set": update_data}
            )
            return {"message": "User updated"}
        except Exception as e:
            api.abort(400, str(e))

    @api.doc("delete_user")
    def delete(self, id):
        """Delete a user"""
        try:
            result = current_app.mongo.db.users.delete_one({"_id": ObjectId(id)})
            if result.deleted_count:
                return {"message": "User deleted"}
            api.abort(404, "User not found")
        except Exception:
            api.abort(400, "Invalid ID format")
