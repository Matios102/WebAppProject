import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.database import get_db
from app.main import app
from app.repositories.auth_repository import create_access_token
from app.models import User, Team
from app.utils.security import get_current_user

client = TestClient(app)

@pytest.fixture
def mock_db_session(mocker):
    session = MagicMock()
    mocker.patch("app.database.get_db", return_value=session)
    return session

@pytest.fixture
def admin_user(mock_db_session):
    admin = User(
        name="admin",
        surname="admin",
        email="admin@example.com",
        role="admin",
        password_hash="password123",
        is_approved=True,
        id=1,
    )
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = admin
    return admin

@pytest.fixture
def test_user(mock_db_session):
    user = User(
        name="user",
        surname="user",
        email="test@example.com",
        role="user",
        password_hash="password123",
        is_approved=True,
        id=2,
    )
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = user
    return user

@pytest.fixture
def database_user(mock_db_session):
    user = User(
        name="user",
        surname="user",
        email="user@example.com",
        role="user",
        password_hash="password123",
        is_approved=True,
        id=3,
    )
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = user
    return user

@pytest.fixture
def manager_user(mock_db_session):
    manager = User(
        name="manager",
        surname="manager",
        email="manager@example.com",
        role="manager",
        password_hash="password123",
        is_approved=True,
        id=4,
    )
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = manager
    return manager

@pytest.fixture
def second_manager_user(mock_db_session):
    manager = User(
        name="manager",
        surname="manager",
        email="manager2@example.com",
        role="manager",
        password_hash="password123",
        is_approved=True,
        id=5,
    )
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = manager
    return manager

@pytest.fixture
def team(mock_db_session):
    team = Team(name="Test Team", id=1)
    mock_db_session.query(Team).filter(Team.id == 1).first.return_value = team
    return team

@pytest.fixture
def team_with_manager(mock_db_session, manager_user):
    team = Team(name="Test Team", manager_id=manager_user.id, id=2)
    mock_db_session.query(Team).filter(Team.id == 2).first.return_value = team
    return team


@pytest.fixture
def valid_admin_token(admin_user):
    return create_access_token({"sub": admin_user.email})

@pytest.fixture
def valid_user_token(test_user):
    return create_access_token({"sub": test_user.email})

@pytest.fixture
def valid_manager_token(manager_user):
    return create_access_token({"sub": manager_user.email})

# Test the "get team" endpoint for a manager
def test_get_team_for_manager(valid_manager_token, manager_user, team):
    def mock_get_current_user():
        return manager_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.get(
        "/api/team", headers={"Authorization": f"Bearer {valid_manager_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Clean up overrides
    app.dependency_overrides = {}

# Test the "get team" endpoint for non-manager
def test_get_team_for_non_manager(valid_user_token, test_user, team):
    def mock_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.get(
        "/api/team", headers={"Authorization": f"Bearer {valid_user_token}"}
    )
    assert response.status_code == 403

    # Clean up overrides
    app.dependency_overrides = {}

# Test the "get all teams" endpoint for an admin
def test_get_all_teams_for_admin(valid_admin_token, admin_user, team):
    def mock_get_current_user():
        return admin_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.get(
        "/api/team/all", headers={"Authorization": f"Bearer {valid_admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # Clean up overrides
    app.dependency_overrides = {}

# Test the "get all teams" endpoint for non-admin
def test_get_all_teams_for_non_admin(valid_user_token, test_user, team):
    def mock_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.get(
        "/api/team/all", headers={"Authorization": f"Bearer {valid_user_token}"}
    )
    assert response.status_code == 403

    # Clean up overrides
    app.dependency_overrides = {}

# Test the "create team" endpoint for an admin
def test_create_team_as_admin(valid_admin_token, admin_user):
    def mock_get_current_user():
        return admin_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.post(
        "/api/team/create",
        json={"team_name": "New Team"},
        headers={"Authorization": f"Bearer {valid_admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Team created"

    # Clean up overrides
    app.dependency_overrides = {}

# Test the "create team" endpoint for non-admin
def test_create_team_as_non_admin(valid_user_token, test_user):
    def mock_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.post(
        "/api/team/create",
        json={"team_name": "New Team"},
        headers={"Authorization": f"Bearer {valid_user_token}"},
    )
    assert response.status_code == 403

    # Clean up overrides
    app.dependency_overrides = {}

# Test the "add team member" endpoint for an admin
def test_add_team_member_as_admin(valid_admin_token, admin_user, team, database_user):
    def mock_get_current_user():
        return admin_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.post(
        "/api/team",
        json={"user_id": database_user.id, "team_id": team.id},
        headers={"Authorization": f"Bearer {valid_admin_token}"},
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "User added to the team"

    app.dependency_overrides = {}

def test_add_team_member_as_non_admin(valid_user_token, test_user, team, database_user, mock_db_session):
    def mock_get_current_user():
        return test_user

    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[get_db] =  mock_db_session  # Mock the db dependency

    response = client.post(
        "/api/team",
        json={"user_id": database_user.id, "team_id": team.id},
        headers={"Authorization": f"Bearer {valid_user_token}"},
    )
    assert response.status_code == 403

    app.dependency_overrides = {}

def test_add_manager_to_team_with_manager(valid_manager_token, admin_user, team_with_manager, second_manager_user, mock_db_session):
    def mock_get_current_user():
        return admin_user

    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[get_db] = lambda: mock_db_session  # Mock the db dependency

    response = client.post(
        "/api/team",
        json={"user_id": second_manager_user.id, "team_id": team_with_manager.id},
        headers={"Authorization": f"Bearer {valid_manager_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Team already has a manager"}

    app.dependency_overrides = {}


