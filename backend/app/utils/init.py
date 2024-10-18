from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRegister
from app.models import Expense, Category, Team
from app.repositories.user_repository import get_user_by_email
from app.repositories.category_repository import get_category_by_name
from app.repositories.auth_repository import create_user


def category_dump(db: Session):
    categories = [
        "Default",
        "Food",
        "Utilities",
        "Transport",
        "Entertainment",
        "Health",
    ]

    for category in categories:
        db_category = get_category_by_name(db, category)
        if not db_category:
            db_category = Category(name=category)
            db.add(db_category)
    db.commit()

def user_dump(db: Session):
    default = get_category_by_name(db, "Default")
    food = get_category_by_name(db, "Food")
    utilities = get_category_by_name(db, "Utilities")

    db_user = get_user_by_email(db, "u@u.uuu")
    expense1 = Expense(
        name="Something",
        amount=100,
        date="2024-10-17",
        category_id=default.id,
        user_id=db_user.id,
    )
    expense2 = Expense(
        name="Food",
        amount=40,
        date="2024-10-01",
        category_id=food.id,
        user_id=db_user.id,
    ) 
    expense3 = Expense(
        name="Electricity",
        amount=70,
        date="2024-09-20",
        category_id=utilities.id,
        user_id=db_user.id,
    )
    expense4 = Expense(
        name="Something",
        amount=80,
        date="2023-02-17",
        category_id=default.id,
        user_id=db_user.id,
    )
    expense5 = Expense(
        name="Food",
        amount=55,
        date="2023-04-01",
        category_id=food.id,
        user_id=db_user.id,
    ) 
    expense6 = Expense(
        name="Electricity",
        amount=70,
        date="2023-09-20",
        category_id=utilities.id,
        user_id=db_user.id,
    )

    user_expenses = db.query(Expense).filter(Expense.user_id == db_user.id).all()
    if not user_expenses:
        db.add(expense1)
        db.add(expense2)
        db.add(expense3)
        db.add(expense4)
        db.add(expense5)
        db.add(expense6)
    db.commit()


def initial_users(db: Session):
    user = UserRegister(
        name="user",
        surname="user",
        email="u@u.uuu",
        password="u",
        )
    
    if not get_user_by_email(db, user.email):
        create_user(db, user)

    db_user = get_user_by_email(db, user.email)
    db_user.role = "user"
    db_user.is_approved = True

    manager = UserRegister(
        name="manager",
        surname="manager",
        email="m@m.mmm",
        password="m",
        )
    
    if not get_user_by_email(db, manager.email):
        create_user(db, manager)

    db_manager = get_user_by_email(db, manager.email)
    db_manager.role = "manager"
    db_manager.is_approved = True

    admin = UserRegister(
        name="admin",
        surname="admin",
        email="a@a.aaa",
        password="a",
        )
    
    if not get_user_by_email(db, admin.email):
        create_user(db, admin)

    db_admin = get_user_by_email(db, admin.email)
    db_admin.role = "admin"
    db_admin.is_approved = True

    approved_user = UserRegister(
        name="approved",
        surname="approved",
        email="approved@approved.com",
        password="approved",
        )
    
    if not get_user_by_email(db, approved_user.email):
        create_user(db, approved_user)
    
    unapproved_user = UserRegister(
        name="unapproved",
        surname="unapproved",
        email="unapproved@unapproved.com",
        password="unapproved",
        )
    
    if not get_user_by_email(db, unapproved_user.email):
        create_user(db, unapproved_user)

    db.commit()


def team_dump(db: Session):
    db_team = db.query(Team).filter(Team.name == "Team").first()
    if not db_team:
        db_team = Team(name="Team")
        db.add(db_team)
        db.commit()



    

