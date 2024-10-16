import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from repositories.auth_repository import create_user
from main import app

client = TestClient(app)

# Mock database dependency
@pytest.fixture
def db_session():
    yield Session() 

@pytest.fixture
def test_user(db_session):
    user_data = {
        "name": "Test",
        "surname": "User",
        "email": "test@example.com",
        "password": "password123"
    }
    create_user(db_session, user_data)
    return user_data

def test_register_user(db_session):
    response = client.post("/register", json={
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "password": "strong_password"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}


def test_register_existing_user(db_session, test_user):
    # Try to register a user with an existing email
    response = client.post("/register", json={
        "name": "Test",
        "surname": "User",
        "email": test_user['email'],
        "password": "password123"
    })
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}
