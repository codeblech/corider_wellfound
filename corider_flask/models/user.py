from datetime import datetime
from bson import ObjectId
import hashlib
import os
import base64


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.salt = os.urandom(16)  # Generate a random salt
        self.password = self._hash_password(password)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def _hash_password(self, password):
        """Hash password using scrypt"""
        hash_bytes = hashlib.scrypt(
            password=password.encode("utf-8"),
            salt=self.salt,
            n=16384,  # CPU/memory cost parameter (2^14)
            r=8,  # Block size parameter
            p=1,  # Parallelization parameter
            maxmem=67108864,  # 64 MB max memory
        )
        return base64.b64encode(hash_bytes).decode("utf-8")

    @staticmethod
    def verify_password(password, hashed_password, salt):
        """Verify a password against a hash"""
        try:
            hash_bytes = hashlib.scrypt(
                password=password.encode("utf-8"),
                salt=salt,
                n=16384,
                r=8,
                p=1,
                maxmem=67108864,
            )
            return base64.b64encode(hash_bytes).decode("utf-8") == hashed_password
        except Exception:
            return False

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "salt": base64.b64encode(self.salt).decode("utf-8"),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
