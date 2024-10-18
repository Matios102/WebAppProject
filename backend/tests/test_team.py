import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.main import app
from app.models import User, Team
from app.repositories.auth_repository import create_access_token
from app.utils.security import get_current_user
from app.core.config import settings

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
    
    yield session
    session.rollback()
    session.close()


@pytest.fixture()
def admin_user(db_session):
    admin = User(
        name="admin",
        surname="admin",
        email="admin@example.com",
        role="admin",
        password_hash="password123",
        is_approved=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture()
def test_user(db_session):
    user = User(
        name="user",
        surname="user",
        email="test@example.com",
        role="user",
        password_hash="password123",
        is_approved=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture()
def manager_user(db_session):
    manager = User(
        name="manager",
        surname="manager",
        email="manager@example.com",
        role="manager",
        password_hash="password123",
        is_approved=True,
    )
    db_session.add(manager)
    db_session.commit()
    db_session.refresh(manager)
    return manager

@pytest.fixture()
def second_manager_user(db_session):
    manager = User(
        name="manager2",
        surname="manager2",
        email="manager2@example.com",
        role="manager",
        password_hash="password123",
        is_approved=True,
    )
    db_session.add(manager)
    db_session.commit()
    db_session.refresh(manager)
    return manager

@pytest.fixture()
def team(db_session, manager_user):
    team = Team(name="Test Team", manager_id=manager_user.id)
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    return team

@pytest.fixture()
def team_with_manager(db_session, manager_user):
    team = Team(name="Test Team with Manager", manager_id=manager_user.id)
    db_session.add(team)
    db_session.commit()
    db_session.refresh(team)
    return team

@pytest.fixture()
def valid_admin_token(admin_user):
    return create_access_token({"sub": admin_user.email})

@pytest.fixture()
def valid_user_token(test_user):
    return create_access_token({"sub": test_user.email})

@pytest.fixture()
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
def test_get_team_for_non_manager( valid_user_token, test_user, team):
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
def test_get_all_teams_for_admin( valid_admin_token, admin_user, team):
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

# Test the "create team" endpoint for an admin
def test_create_team_as_admin( valid_admin_token, admin_user):
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

# Test the "add team member" endpoint for an admin
def test_add_team_member_as_admin( valid_admin_token, admin_user, team, test_user):
    def mock_get_current_user():
        return admin_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.post(
        "/api/team",
        json={"user_id": test_user.id, "team_id": team.id},
        headers={"Authorization": f"Bearer {valid_admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User added to the team"

    # Clean up overrides
    app.dependency_overrides = {}

# Test the "add manager to team with manager" endpoint
def test_add_manager_to_team_with_manager( valid_manager_token, admin_user, team_with_manager, second_manager_user):
    def mock_get_current_user():
        return admin_user

    app.dependency_overrides[get_current_user] = mock_get_current_user

    response = client.post(
        "/api/team",
        json={"user_id": second_manager_user.id, "team_id": team_with_manager.id},
        headers={"Authorization": f"Bearer {valid_manager_token}"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Team already has a manager"}
