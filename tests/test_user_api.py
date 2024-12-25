import pytest
from app.main import create_app
from app.core.config import Config
from flask_jwt_extended import create_access_token
from app.models.user import User
from bson import ObjectId

@pytest.fixture
def app():
    app = create_app()
    # Use a dedicated test database
    test_db_name = "test_user_management"
    app.config.update({
        "TESTING": True,
        "MONGODB_URI": f"mongodb://localhost:27017/{test_db_name}",
        "MONGODB_DB": test_db_name,
        "JWT_SECRET_KEY": "test-secret-key"
    })
    
    # Drop the test database before starting
    with app.app_context():
        app.mongo.client.drop_database(test_db_name)
    
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            # Clear all collections before each test
            app.mongo.users.delete_many({})
            # Verify the collection is empty
            assert app.mongo.users.count_documents({}) == 0
        yield client

def get_headers(user_id=None):
    token = create_access_token(identity=user_id) if user_id else create_access_token(identity="testuser")
    return {
        "Authorization": f"Bearer {token}"
    }

def test_create_user(client):
    response = client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_all_users(client):
    # Create a user first
    client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    response = client.get("/api/v1/users", headers=get_headers())
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["email"] == "test@example.com"

def test_get_user_by_id(client):
    # Create a user first
    response = client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    user_id = response.get_json()["id"]
    response = client.get(f"/api/v1/users/{user_id}", headers=get_headers(user_id))
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == user_id

def test_update_user(client):
    # Create a user first
    response = client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    user_id = response.get_json()["id"]
    # Update the user
    response = client.put(f"/api/v1/users/{user_id}", json={
        "name": "Updated User"
    }, headers=get_headers(user_id))
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated User"

def test_delete_user(client):
    # Create a user first
    response = client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    user_id = response.get_json()["id"]
    # Delete the user
    response = client.delete(f"/api/v1/users/{user_id}", headers=get_headers(user_id))
    assert response.status_code == 204
    # Verify deletion
    response = client.get(f"/api/v1/users/{user_id}", headers=get_headers(user_id))
    assert response.status_code == 404

def test_login_user(client):
    # Create a user first
    client.post("/api/v1/users", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    # Attempt to login
    response = client.post("/api/v1/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data 