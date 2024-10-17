# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import MagicMock, patch
# from app.main import app
# from app.models import Category, User, Expense
# from app.utils.jwt_handler import create_access_token
# from app.utils.security import get_current_user

# client = TestClient(app)


# @pytest.fixture
# def mock_db_session(mocker):
#     session = MagicMock()
#     mocker.patch("app.dependencies.get_db", return_value=session)
#     return session


# @pytest.fixture
# def auth_header():
#     token = create_access_token({"sub": "testuser"})
#     return {"Authorization": f"Bearer {token}"}


# @pytest.fixture
# def category1(mock_db_session):
#     category = Category(id=1, name="test category 1")
#     mock_db_session.query(Category).filter_by.return_value.first.return_value = category
#     return category


# @pytest.fixture
# def approved_user(mock_db_session):
#     user = User(id=1, name="user", surname="user", email="approved@example.com", role="user", password_hash="password123", is_approved=True)
#     mock_db_session.query(User).filter_by.return_value.first.return_value = user
#     return user


# @pytest.fixture
# def unapproved_user(mock_db_session):
#     user = User(id=2, name="user", surname="user", email="unapproved@example.com", role="user", password_hash="password123", is_approved=False)
#     mock_db_session.query(User).filter_by.return_value.first.return_value = user
#     return user


# @pytest.fixture
# def expense_cat1(mock_db_session, approved_user, category1):
#     expense = Expense(id=1, name="test expense", amount=100.0, date="2021-01-01", user_id=approved_user.id, category_id=category1.id)
#     mock_db_session.query(Expense).filter_by.return_value.first.return_value = expense
#     return expense


# @pytest.fixture
# def valid_approved_user_token(approved_user):
#     return create_access_token({"sub": approved_user.email})


# @pytest.fixture
# def valid_unapproved_token(unapproved_user):
#     return create_access_token({"sub": unapproved_user.email})


# def test_create_expense(mock_db_session, valid_approved_user_token, category1, approved_user):
#     def mock_get_current_user():
#         return approved_user

#     app.dependency_overrides[get_current_user] = mock_get_current_user

#     expense_data = {
#         "name": "Test Expense",
#         "amount": 100.0,
#         "category_id": category1.id,
#         "date": "2021-01-01",
#         "user_id": approved_user.id
#     }
#     response = client.post("/api/expenses/", json=expense_data, headers={"Authorization": f"Bearer {valid_approved_user_token}"})
#     assert response.status_code == 200
#     assert response.json()["message"] == "Expense created successfully"

#     app.dependency_overrides = {}


# def test_get_expense(mock_db_session, auth_header, expense_cat1):
#     expense_id = expense_cat1.id
#     response = client.get(f"/api/expenses/{expense_id}", headers=auth_header)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == expense_id


# def test_update_expense(mock_db_session, auth_header, expense_cat1):
#     expense_id = expense_cat1.id
#     update_data = {
#         "name": "Updated Expense",
#         "amount": 150.0,
#         "description": "Updated Description"
#     }
#     response = client.put(f"/api/expenses/{expense_id}", json=update_data, headers=auth_header)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == update_data["name"]
#     assert data["amount"] == update_data["amount"]
#     assert data["description"] == update_data["description"]


# def test_delete_expense(mock_db_session, auth_header, expense_cat1):
#     expense_id = expense_cat1.id
#     response = client.delete(f"/api/expenses/{expense_id}", headers=auth_header)
#     assert response.status_code == 204
#     # Verify the expense is deleted
#     response = client.get(f"/api/expenses/{expense_id}", headers=auth_header)
#     assert response.status_code == 404
