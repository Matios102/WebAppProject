from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRegister
from app.models import Expense, Category, Team, User
from app.repositories.user_repository import get_user_by_email
from app.repositories.category_repository import get_category_by_name
from app.repositories.auth_repository import create_user
from random import randint, choice


def category_dump(db: Session):
    categories = [
        "Default", "Food", "Utilities", "Transport", "Entertainment", "Health", "Travel", "Education",
        "Shopping", "Rent", "Insurance", "Subscriptions", "Gifts", "Charity", "Pets", "Sports"
    ]

    for category in categories:
        if not get_category_by_name(db, category):
            db.add(Category(name=category))
    db.commit()


def initial_users(db: Session):
    users = []

    # Create main users
    main_users = [
        {"name": "user", "surname": "user", "email": "user@user.com", "password": "user", "role": "user", "is_approved": True},
        {"name": "manager", "surname": "manager", "email": "manager@manager.com", "password": "manager", "role": "manager", "is_approved": True},
        {"name": "admin", "surname": "admin", "email": "admin@admin.com", "password": "admin", "role": "admin", "is_approved": True},
    ]
    users.extend(main_users)

    # Generate additional users
    for i in range(1, 51):
        users.append({
            "name": f"user{i}",
            "surname": f"surname{i}",
            "email": f"user{i}@example.com",
            "password": f"password{i}",
            "role": "user",
            "is_approved": True,
        })

    for user_data in users:
        user_reg = UserRegister(
            name=user_data["name"],
            surname=user_data["surname"],
            email=user_data["email"],
            password=user_data["password"]
        )
        if not get_user_by_email(db, user_reg.email):
            create_user(db, user_reg)

        db_user = get_user_by_email(db, user_reg.email)
        db_user.role = user_data["role"]
        db_user.is_approved = user_data["is_approved"]

    db.commit()


def team_dump(db: Session):
    team_names = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Omega"]

    for name in team_names:
        if not db.query(Team).filter(Team.name == name).first():
            db.add(Team(name=name))

    db.commit()


def user_expense_dump(db: Session):
    categories = {cat.name: cat for cat in db.query(Category).all()}
    all_users = db.query(User).all()

    expenses_names = ["Groceries", "Restaurant", "Internet Bill", "Electricity", "Movie", "Gym", "Train Ticket",
                      "Vacation", "Books", "Clothes", "Apartment Rent", "Health Insurance", "Netflix", "Spotify",
                      "Birthday Gift", "Donation", "Pet Food", "Football Tickets"]

    for user in all_users:
        user_expense_count = randint(10, 30)
        for _ in range(user_expense_count):
            expense = Expense(
                name=choice(expenses_names),
                amount=randint(10, 500),
                date=f"2024-{randint(1,12):02}-{randint(1,28):02}",
                category_id=categories[choice(list(categories.keys()))].id,
                user_id=user.id,
            )
            db.add(expense)

    db.commit()


def full_dump(db: Session):
    category_dump(db)
    initial_users(db)
    team_dump(db)
    user_expense_dump(db)
