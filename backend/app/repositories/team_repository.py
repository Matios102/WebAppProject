from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Category, Expense, Team, User
from app.schemas.user_schema import UserDisplay

def get_team(db: Session, current_user: User) -> list[UserDisplay]:
    if current_user.role != "manager":
        raise PermissionError("You are not a manager")
    return db.query(User).filter(User.team_id == current_user.team_id).all()

def create_team(db: Session, team_name: str, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    team = Team(name=team_name)
    db.add(team)
    db.commit()
    db.refresh(team)

def get_all_teams(db: Session, current_user: User) -> list[dict]:
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")

    teams = db.query(Team).all()
    result = []

    for team in teams:
        users = db.query(User).filter(User.team_id == team.id).all()
        manager = db.query(User).filter(User.id == team.manager_id).first()

        manager_info = None
        user_info = []
        if users is not None:
            user_info = [
                {
                    "id": user.id,
                    "name": user.name,
                    "surname": user.surname,
                    "email": user.email,
                    "role": user.role,
                }
                for user in users
            ]
        if manager is not None:
            manager_info = {
                "id": manager.id,
                "name": manager.name,
                "surname": manager.surname,
                "email": manager.email,
                "role": manager.role,
            }

        team_info = {"team": team, "manager": manager_info, "users": user_info}

        result.append(team_info)

    return result

def delete_team(db: Session, team_id: int, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise ValueError("Team not found")

    users_in_team = db.query(User).filter(User.team_id == team.id).all()
    for user in users_in_team:
        user.team_id = None

    db.delete(team)
    db.commit()

def add_team_member(db: Session, user_id: int, team_id: int, current_user: User):

    print(db)
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    team = db.query(Team).filter(Team.id == team_id).first()
    print(team)
    if team is None:
        raise ValueError("Team not found")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("User not found")
    if user.team_id != None:
        raise ValueError("User is already in a team")
    if user.role == "manager" and team.manager_id != None:
        raise ValueError("Team already has a manager")

    if user.role == "manager":
        team.manager_id = user_id
    else:
        user.team_id = team_id
    db.commit()
    db.refresh(user)

def delete_team_member(db: Session, user_id: int, team_id: int, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise ValueError("Team not found")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ValueError("User not found")
    if user.team_id != team_id and user.role != "manager":
        raise ValueError("User is not in a team")
    if user.role == "manager":
        team.manager_id = None

    user.team_id = None
    db.commit()
    db.refresh(user)

def get_team_expenses(db: Session, current_user: User) -> dict:
    if current_user.role != "manager":
        raise PermissionError("You are not a manager")
    
    existing_team = db.query(Team).filter(Team.manager_id == current_user.id).first()
    if not existing_team:
        raise ValueError("No team found for the manager")

    expenses = (
        db.query(
            User.id.label("user_id"),
            User.name.label("user_name"),
            User.surname.label("user_surname"),
            Category.name.label("category_name"),
            func.sum(Expense.amount).label("total_expenses"),
        )
        .join(User, User.id == Expense.user_id)
        .join(Category, Category.id == Expense.category_id)
        .filter(User.team_id == existing_team.id)
        .group_by(User.id, User.name, User.surname, Category.name)
        .all()
    )

    team_expenses = {}
    for expense in expenses:
        if expense.user_id not in team_expenses:
            team_expenses[expense.user_id] = {
                "name": expense.user_name,
                "surname": expense.user_surname,
                "total_spendings": 0,
                "spendings_by_category": {}
            }
        team_expenses[expense.user_id]["total_spendings"] += expense.total_expenses
        team_expenses[expense.user_id]["spendings_by_category"][expense.category_name] = expense.total_expenses

    return team_expenses

def get_team_expenses_by_category(db: Session, current_user: User) -> dict:
    if current_user.role != "manager":
        raise PermissionError("You are not a manager")

    expenses = (
        db.query(Category.name, func.sum(Expense.amount).label("total_amount"))
        .join(User)
        .join(Category)
        .filter(User.team_id == current_user.team_id)
        .group_by(Category.name)
        .all()
    )

    return {category: total_amount for category, total_amount in expenses}

def get_users_without_team(
    db: Session, current_user: User, name_or_surname: str
) -> list[UserDisplay]:
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    query = db.query(User).filter(
        User.team_id == None, User.role != "admin", User.is_approved == True
    )

    if name_or_surname:
        query = query.filter(
            (User.name.contains(name_or_surname))
            | (User.surname.contains(name_or_surname))
        )

    users = query.all()

    user_display_list = [
        UserDisplay(
            id=user.id,
            name=user.name,
            surname=user.surname,
            email=user.email,
        )
        for user in users if not db.query(Team).filter(Team.manager_id == user.id).first()
    ]
    
    return user_display_list
