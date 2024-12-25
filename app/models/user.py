from datetime import datetime, timezone
from bson import ObjectId
from app.core.security import hash_password

class User:
    def __init__(self, name, email, password, _id=None, created_at=None):
        self._id = _id if _id else str(ObjectId())
        self.name = name
        self.email = email
        self.password = hash_password(password)
        self.created_at = created_at if created_at else datetime.now(timezone.utc)

    @staticmethod
    def from_db(data):
        if not data:
            return None
        return User(
            _id=str(data["_id"]),
            name=data["name"],
            email=data["email"],
            password=data["password"],
            created_at=data["created_at"]
        )

    def to_dict(self):
        return {
            "_id": ObjectId(self._id),
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at
        }

    @property
    def id(self):
        return self._id