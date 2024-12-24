from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = environ.get("MONGO_URI", "mongodb://mongodb:27017/")
    MONGO_DB = environ.get("MONGO_DB", "user_db")
    DEBUG = environ.get("FLASK_DEBUG", True)
