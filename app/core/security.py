from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)

def create_token(user_id: str) -> str:
    return create_access_token(identity=user_id)