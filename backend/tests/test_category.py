import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models import Category, User
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
def approved_admin(db_session):
    user = User(name="admin", surname="admin", email="admin@example.com", role="admin", password_hash="password123", is_approved=True)
    db_session.add(user)
    db_session.commit()
    return user

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
def category1(db_session):
    category = Category(name="test category 1")
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def default_category(db_session):
    category = Category(name="default")
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def existing_category(db_session):
    category = Category(name="Existing Category")
    db_session.add(category)
    db_session.commit()
    return category

@pytest.fixture
def valid_approved_admin_token(approved_admin):
    return create_access_token({"sub": approved_admin.email})

@pytest.fixture
def valid_approved_user_token(approved_user):
    return create_access_token({"sub": approved_user.email})

@pytest.fixture
def valid_unapproved_token(unapproved_user):
    return create_access_token({"sub": unapproved_user.email})

# Test getting categories for admin
def test_get_categories_for_admin(valid_approved_admin_token, db_session):
    category = Category(name="Admin Category")
    db_session.add(category)
    db_session.commit()

    response = client.get("/api/admin/categories", headers={"Authorization": f"Bearer {valid_approved_admin_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

# Test getting categories for approved user
def test_get_categories_for_approved_user(valid_approved_user_token, db_session):
    category = Category(name="User Category")
    db_session.add(category)
    db_session.commit()

    response = client.get("/api/categories", headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

# Test getting categories for unapproved user
def test_get_categories_for_unapproved_user(valid_unapproved_token):
    response = client.get("/api/categories", headers={"Authorization": f"Bearer {valid_unapproved_token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not approved"

# Test creating a category as admin
def test_create_category(valid_approved_admin_token):
    category_data = {"category_name": "New Admin Category"}
    response = client.post("/api/categories", json=category_data, headers={"Authorization": f"Bearer {valid_approved_admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Category created"

# Test creating a category as an approved user (should fail)
def test_create_category_as_user(valid_approved_user_token):
    category_data = {"category_name": "New User Category"}
    response = client.post("/api/categories", json=category_data, headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not an admin"

# Test updating a category as admin
def test_update_category(valid_approved_admin_token, category1):
    category_data = {"category_name": "Updated Category", "category_id": category1.id}
    response = client.put(f"/api/categories/{category1.id}", json=category_data, headers={"Authorization": f"Bearer {valid_approved_admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Category updated"

# Test updating a category as user (should fail)
def test_update_category_as_user(valid_approved_user_token, category1):
    category_data = {"category_name": "Updated Category", "category_id": category1.id}
    response = client.put(f"/api/categories/{category1.id}", json=category_data, headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not an admin"

# Test deleting a category as admin
def test_delete_category(valid_approved_admin_token, category1):
    response = client.delete(f"/api/categories/{category1.id}", headers={"Authorization": f"Bearer {valid_approved_admin_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Category deleted"

# Test deleting a category as user (should fail)
def test_delete_category_as_user(valid_approved_user_token, category1):
    response = client.delete(f"/api/categories/{category1.id}", headers={"Authorization": f"Bearer {valid_approved_user_token}"})
    assert response.status_code == 403
    assert response.json()["detail"] == "You are not an admin"

# Test creating a category with existing name
def test_create_existing_category(valid_approved_admin_token, category1):
    category_data = {"category_name": "test category 1"}
    response = client.post("/api/categories", json=category_data, headers={"Authorization": f"Bearer {valid_approved_admin_token}"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Category already exists"

# Test updating to an existing category name
def test_update_to_existing_category(valid_approved_admin_token, category1, existing_category):
    category_data = {"category_name": existing_category.name, "category_id": category1.id}
    response = client.put(f"/api/categories/{category1.id}", json=category_data, headers={"Authorization": f"Bearer {valid_approved_admin_token}"})
    assert response.status_code == 409
    assert response.json()["detail"] == "Category already exists"

# Test deleting default category (assuming ID 1 is default)
def test_delete_default_category(valid_approved_admin_token, default_category):
    response = client.delete(f"/api/categories/{default_category.id}", headers={"Authorization": f"Bearer {valid_approved_admin_token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Cannot delete default category"

# Test getting categories without approval
def test_get_categories_without_approval(unapproved_user):
    response = client.get("/api/admin/categories", headers={"Authorization": f"Bearer {valid_unapproved_token}"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
