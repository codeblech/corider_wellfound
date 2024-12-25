from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_TITLE = "User Management API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # MongoDB settings
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DB = os.getenv("MONGODB_DB", "user_management")
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)