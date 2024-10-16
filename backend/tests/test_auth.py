import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.repositories.auth_repository import create_user
from app.schemas.user_schema import UserRegister
from app.models import User

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("postgresql://postgres:password@localhost:5432/dough")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    session.execute(text("TRUNCATE TABLE expenses RESTART IDENTITY CASCADE"))
    session.execute(text("TRUNCATE TABLE categories RESTART IDENTITY CASCADE"))
    session.execute(text("TRUNCATE TABLE teams RESTART IDENTITY CASCADE"))
    session.commit()
    
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def test_user(db_session):
    user_data = UserRegister(
        name="Test", surname="User", email="test@example.com", password="password123"
    )
    
    db_session.query(User).filter(User.email == "test@example.com").delete()
    db_session.commit()
    
    create_user(db_session, user_data)
    
    yield user_data
    
    db_session.query(User).filter(User.email == "test@example.com").delete()
    db_session.commit()

def test_register_user(db_session):
    response = client.post(
        "/register",
        json={
            "name": "John",
            "surname": "Doe",
            "email": "john.doe@example.com",
            "password": "strong_password",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}
    
    db_session.query(User).filter(User.email == "john.doe@example.com").delete()
    db_session.commit()

def test_register_existing_user(db_session, test_user):
    response = client.post(
        "/register",
        json={
            "name": "Test",
            "surname": "User",
            "email": test_user.email,
            "password": "password123",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}

def test_login_success(db_session, test_user):
    response = client.post(
        "/token", data={"username": test_user.email, "password": test_user.password}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert "role" in json_data
    assert json_data["token_type"] == "bearer"

def test_login_invalid_credentials(db_session, test_user):
    response = client.post(
        "/token", data={"username": test_user.email, "password": "wrong_password"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}

def test_check_token_success(db_session, mocker):
    mocker.patch(
        "app.repositories.auth_repository.decode_access_token",
        return_value={"sub": "test@example.com"},
    )
    mocker.patch(
        "app.repositories.auth_repository.check_user_approval", return_value=True
    )
    mocker.patch("app.repositories.auth_repository.get_user_role", return_value="admin")
    
    response = client.post("/check-token", json={"token": "valid_token"})
    assert response.status_code == 200
    assert response.json() == {"role": "admin", "is_approved": True}

def test_check_token_invalid(db_session, mocker):
    mocker.patch(
        "app.repositories.auth_repository.decode_access_token", return_value=None
    )
    
    response = client.post("/check-token", json={"token": "invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
