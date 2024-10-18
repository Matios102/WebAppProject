import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from app.main import app
from app.models import Team, User
from app.utils.jwt_handler import create_access_token
from app.core.config import settings

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(settings.TEST_DATABASE_URL)
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
    yield admin


@pytest.fixture
def test_user(db_session):
    user = User(
        name="user",
        surname="user",
        email="test+1@example.com",
        role="user",
        password_hash="password123",
        is_approved=False,
    )
    db_session.add(user)
    db_session.commit()
    yield user


@pytest.fixture
def user_with_team(db_session, team_with_manager_and_user):
    user = User(
        name="user",
        surname="user",
        email="user_team@example.com",
        role="user",
        password_hash="password123",
        is_approved=True,
        team_id=team_with_manager_and_user.id,
    )
    db_session.add(user)
    db_session.commit()
    yield user


@pytest.fixture
def team_with_manager_and_user(db_session, admin_user):
    team = Team(
        name="Test Team",
        manager_id=admin_user.id,
    )
    db_session.add(team)
    db_session.commit()

    user = User(
        name="team_user",
        surname="user",
        email="team_user@example.com",
        role="user",
        password_hash="password123",
        is_approved=True,
    )
    db_session.add(user)
    db_session.commit()

    user.team_id = team.id
    db_session.commit()

    yield team


@pytest.fixture
def valid_token(admin_user):
    return create_access_token({"sub": admin_user.email})


@pytest.fixture
def current_user(db_session, admin_user):
    return admin_user


@pytest.fixture
def valid_token(admin_user):
    return create_access_token({"sub": admin_user.email})


@pytest.fixture
def current_user(db_session, admin_user):
    return admin_user


def test_get_users(db_session, mocker, current_user, valid_token):
    mocker.patch(
        "app.repositories.user_repository.get_filtered_users",
        return_value=[current_user],
    )

    response = client.get(
        "/api/users", headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == current_user.email


def test_approve_user(db_session, mocker, current_user, test_user, valid_token):
    mocker.patch("app.repositories.user_repository.approve_user", return_value=None)

    response = client.put(
        f"/api/users/approve/{test_user.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "User approved successfully"}


def test_change_user_role(db_session, mocker, current_user, test_user, valid_token):
    mocker.patch("app.repositories.user_repository.change_user_role", return_value=None)

    response = client.put(
        f"/api/users/change-role/{test_user.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "User role changed successfully"}


def test_delete_user(db_session, mocker, current_user, test_user, valid_token):
    mocker.patch("app.repositories.user_repository.delete_user", return_value=None)

    response = client.delete(
        f"/api/users/{test_user.id}", headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}


def test_get_users_permission_error(db_session, mocker, current_user, valid_token):
    current_user.role = "user"
    mocker.patch(
        "app.repositories.user_repository.get_filtered_users",
        side_effect=PermissionError("You are not an admin"),
    )
    mocker.patch("app.utils.security.get_current_user", return_value=current_user)

    response = client.get(
        "/api/users", headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "You are not an admin"}


def test_approve_user_not_found(db_session, mocker, current_user, valid_token):
    mocker.patch(
        "app.repositories.user_repository.approve_user",
        side_effect=ValueError("User not found"),
    )
    mocker.patch("app.utils.security.get_current_user", return_value=current_user)

    response = client.put(
        f"/api/users/approve/999", headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_change_user_role_permission_error(
    db_session, mocker, current_user, valid_token
):
    mocker.patch(
        "app.repositories.user_repository.change_user_role",
        side_effect=PermissionError("You are not an admin"),
    )
    mocker.patch("app.utils.security.get_current_user", return_value=current_user)

    response = client.put(
        f"/api/users/change-role/{current_user.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "You are not an admin"}


def test_change_user_role_in_a_team_with_manager(
    db_session, mocker, current_user, user_with_team, valid_token
):
    mocker.patch(
        "app.repositories.user_repository.change_user_role",
        side_effect=PermissionError("User is in a team with a manager"),
    )
    mocker.patch("app.utils.security.get_current_user", return_value=current_user)

    response = client.put(
        f"/api/users/change-role/{user_with_team.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "User is in a team with a manager"}


def test_delete_user_not_found(db_session, mocker, current_user, valid_token):
    mocker.patch(
        "app.repositories.user_repository.delete_user",
        side_effect=ValueError("User not found"),
    )
    mocker.patch("app.utils.security.get_current_user", return_value=current_user)

    response = client.delete(
        f"/api/users/{999}", headers={"Authorization": f"Bearer {valid_token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user_permission_error(db_session, mocker, current_user, valid_token):
    current_user.role = "user"
    mocker.patch(
        "app.repositories.user_repository.delete_user",
        side_effect=PermissionError("You don't have permission to delete this user"),
    )
    mocker.patch("app.utils.security.get_current_user", return_value=current_user)

    response = client.delete(
        f"/api/users/{current_user.id}",
        headers={"Authorization": f"Bearer {valid_token}"},
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You don't have permission to delete this user"
    }
