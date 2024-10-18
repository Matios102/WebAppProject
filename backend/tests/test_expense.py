import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Category, User, Expense
from app.utils.jwt_handler import create_access_token
from app.core.config import settings

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(settings.TEST_DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    session.execute(text("TRUNCATE TABLE expenses RESTART IDENTITY CASCADE"))
    session.execute(text("TRUNCATE TABLE categories RESTART IDENTITY CASCADE"))
    session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    session.commit()
    
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def auth_header():
    token = create_access_token({"sub": "testuser"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def category1(db_session):
    category = Category(name="test category 1")
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def approved_user(db_session):
    user = User(name="user", surname="user", email="approved@example.com", role="user", password_hash="password123", is_approved=True)
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def unapproved_user(db_session):
    user = User(name="user", surname="user", email="unapproved@example.com", role="user", password_hash="password123", is_approved=False)
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def admin_user(db_session):
    user = User(name="admin", surname="admin", email="admin@example.com", role="admin", password_hash="password123", is_approved=True)
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def expense_cat1(db_session, approved_user, category1):
    expense = Expense(name="test expense", amount=100.0, date="2021-01-01", user_id=approved_user.id, category_id=category1.id)
    db_session.add(expense)
    db_session.commit()
    return expense

@pytest.fixture
def valid_approved_user_token(approved_user):
    return create_access_token({"sub": approved_user.email})

@pytest.fixture
def valid_unapproved_token(unapproved_user):
    return create_access_token({"sub": unapproved_user.email})

@pytest.fixture
def valid_admin_token(admin_user):
    return create_access_token({"sub": admin_user.email})

# Test creating an expense
def test_create_expense(valid_approved_user_token, category1, approved_user):
    expense_data = {
        "name": "Test Expense",
        "amount": 100.0,
        "category_id": category1.id,
        "date": "2021-01-01",
        "user_id": approved_user.id
    }
    response = client.post("/api/expenses/", json=expense_data, headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Expense created successfully"

    app.dependency_overrides.clear()

# Test getting an expense
def test_get_expenses(auth_header, expense_cat1, valid_approved_user_token):
    response = client.get("/api/expenses/", headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["id"] == expense_cat1.id

# Test updating an expense
def test_update_expense(expense_cat1, valid_approved_user_token):
    expense_id = expense_cat1.id
    update_data = {
        "name": "Updated Expense",
        "amount": 150.0,
    }
    response = client.put(f"/api/expenses/{expense_id}", json=update_data, headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["amount"] == update_data["amount"]

# Test deleting an expense
def test_delete_expense(expense_cat1, valid_approved_user_token):
    expense_id = expense_cat1.id
    response = client.delete(f"/api/expenses/{expense_id}", headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 200


# Test for admin trying to create an expense
def test_admin_create_expense(db_session, category1, admin_user, valid_admin_token):
    expense_data = {
        "name": "Admin Test Expense",
        "amount": 200.0,
        "category_id": category1.id,
        "date": "2021-01-02",
        "user_id": admin_user.id
    }
    response = client.post("/api/expenses/", json=expense_data, headers={"Authorization": f"Bearer {valid_admin_token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Admins cannot have expenses"


# Test for not approved user trying to create an expense
def test_create_expense_unapproved_user(valid_unapproved_token, category1, unapproved_user):
    expense_data = {
        "name": "Unapproved User Expense",
        "amount": 100.0,
        "category_id": category1.id,
        "date": "2021-01-01",
        "user_id": unapproved_user.id
    }
    response = client.post("/api/expenses/", json=expense_data, headers={"Authorization": f"Bearer {valid_unapproved_token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "User is not approved yet"
