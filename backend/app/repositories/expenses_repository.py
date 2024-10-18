from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Category, Expense, User
from app.schemas.expense_schema import (
    ExpenseList,
    ExpenseUpdate,
    ExpenseView,
    ExpenseCreate,
)


def get_expenses(db: Session, current_user: User, expense_name: str, expense_amount: float, expense_category: int, expense_date:datetime.date ) -> list[ExpenseList]:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")

    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")

    query = (
        db.query(
            Expense.id,
            Expense.name,
            Expense.amount,
            Expense.date,
            Category.name.label("category_name"),
            Category.id.label("category_id"),
        )
        .join(Category, Expense.category_id == Category.id)
        .filter(Expense.user_id == current_user.id)
    )

    if expense_name:
        query = query.filter(Expense.name.contains(expense_name))
    if expense_amount:
        query = query.filter(Expense.amount == expense_amount)
    if expense_category:
        query = query.filter(Category.id == expense_category)
    if expense_date:
        query = query.filter(Expense.date == expense_date)

    expenses = query.all()


    return [
        ExpenseList(
            id=expense.id,
            name=expense.name,
            amount=expense.amount,
            date=expense.date,
            category_name=expense.category_name,
            category_id=expense.category_id,
        )
        for expense in expenses
    ]


def view_expense(db: Session, expense_id: int, current_user: User) -> ExpenseView:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")

    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")

    db_expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not db_expense:
        raise ValueError("Expense not found")

    category_name = (
        db.query(Category.name).filter(Category.id == db_expense.category_id).first()[0]
    )

    return ExpenseView(
        name=db_expense.name,
        amount=db_expense.amount,
        date=db_expense.date,
        category_name=category_name,
    )


def create_expense(db: Session, expense: ExpenseCreate, current_user: User):
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")

    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    
    if(expense.amount < 0):
        raise ValueError("Amount cannot be negative")
    
    if not expense.category_id:
        expense.category_id = 1

    category_id = (
        db.query(Category.id).filter(Category.id == expense.category_id).scalar()
    )
    if not category_id:
        raise ValueError("Category not found")

    db_expense = Expense(
        name=expense.name,
        amount=expense.amount,
        category_id=category_id,
        date=expense.date,
        user_id=current_user.id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)


def update_expense(
    db: Session, expense_id: int, expense_update: ExpenseUpdate, current_user: User
) -> ExpenseView:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")

    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    
    if(expense_update.amount < 0):
        raise ValueError("Amount cannot be negative")
    
    db_expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not db_expense: 
        raise ValueError("Expense not found")

    if expense_update.name is not None:
        db_expense.name = expense_update.name
    if expense_update.amount is not None:
        db_expense.amount = expense_update.amount
    if expense_update.date is not None:
        db_expense.date = expense_update.date
    if expense_update.category_id is not None:
        db_expense.category_id = expense_update.category_id

    db.commit()
    db.refresh(db_expense)

    category_name = (
        db.query(Category.name).filter(Category.id == db_expense.category_id).first()[0]
    )

    return ExpenseView(
        name=db_expense.name,
        amount=db_expense.amount,
        date=db_expense.date,
        category_name=category_name,
    )


def delete_expense(db: Session, expense_id: int, current_user: User):
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    db_expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not db_expense:
        raise ValueError("Expense not found")

    db.delete(db_expense)
    db.commit()



def get_total_spendings(db: Session, current_user: User) -> dict:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if not current_user.is_approved:
        raise PermissionError("User is not approved yet")

    # Sum of expenses for the last 7 days (week)
    week = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.date >= datetime.now() - timedelta(days=7),
    ).scalar()

    # Sum of expenses for the last 30 days (month)
    month = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.date >= datetime.now() - timedelta(days=30),
    ).scalar()

    # Sum of expenses for the last 365 days (year)
    year = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.date >= datetime.now() - timedelta(days=365),
    ).scalar()

    # Sum of all expenses
    total = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id
    ).scalar()

    return {
        "week": week if week else 0,
        "month": month if month else 0,
        "year": year if year else 0,
        "total": total if total else 0,
    }



def get_total_spendings_by_category(
    db: Session, current_user: User, category_id: int, period: str
) -> float:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    if period == "week":
        return (
            db.query(Expense)
            .filter(
                Expense.user_id == current_user.id,
                Expense.category_id == category_id,
                Expense.date >= datetime.now() - datetime.timedelta(days=7),
            )
            .with_entities(func.sum(Expense.amount))
            .scalar()
        )
    elif period == "month":
        return (
            db.query(Expense)
            .filter(
                Expense.user_id == current_user.id,
                Expense.category_id == category_id,
                Expense.date >= datetime.now() - datetime.timedelta(days=30),
            )
            .with_entities(func.sum(Expense.amount))
            .scalar()
        )
    elif period == "year":
        return (
            db.query(Expense)
            .filter(
                Expense.user_id == current_user.id,
                Expense.category_id == category_id,
                Expense.date >= datetime.now() - datetime.timedelta(days=365),
            )
            .with_entities(func.sum(Expense.amount))
            .scalar()
        )
    else:
        raise ValueError("Invalid period")


def get_monthly_comparison(db: Session, current_user: User) -> dict:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    last_month = current_month - 1 if current_month != 1 else 12
    last_year = current_year if current_month != 1 else current_year - 1

    current_month_spendings = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id,
            Expense.date >= datetime(current_year, current_month, 1),
            Expense.date < datetime(current_year, current_month + 1, 1),
        )
        .with_entities(func.sum(Expense.amount))
        .scalar()
    )
    last_month_spendings = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id,
            Expense.date >= datetime(last_year, last_month, 1),
            Expense.date < datetime(last_year, last_month + 1, 1),
        )
        .with_entities(func.sum(Expense.amount))
        .scalar()
    )

    return {
        "current_month": current_month_spendings if current_month_spendings else 0,
        "last_month": last_month_spendings if last_month_spendings else 0,
    }


def get_monthly_comparison_by_category(
    db: Session, current_user: User, category_id: int
) -> dict:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    last_month = current_month - 1 if current_month != 1 else 12
    last_year = current_year if current_month != 1 else current_year - 1

    current_month_spendings = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id,
            Expense.category_id == category_id,
            Expense.date >= datetime(current_year, current_month, 1),
            Expense.date < datetime(current_year, current_month + 1, 1),
        )
        .with_entities(func.sum(Expense.amount))
        .scalar()
    )
    last_month_spendings = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id,
            Expense.category_id == category_id,
            Expense.date >= datetime(last_year, last_month, 1),
            Expense.date < datetime(last_year, last_month + 1, 1),
        )
        .with_entities(func.sum(Expense.amount))
        .scalar()
    )

    return {
        "current_month": current_month_spendings if current_month_spendings else 0,
        "last_month": last_month_spendings if last_month_spendings else 0,
    }


def get_yearly_comparison(db: Session, current_user: User) -> dict:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    
    current_year = datetime.now().year
    last_year = current_year - 1

    def get_monthly_expenses(year):
        monthly_expenses = {}
        for month in range(1, 13):
            month_start = datetime(year, month, 1)
            month_end = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
            monthly_expenses[month] = (
                db.query(func.sum(Expense.amount))
                .filter(
                    Expense.user_id == current_user.id,
                    Expense.date >= month_start,
                    Expense.date < month_end,
                )
                .scalar() or 0
            )
        return monthly_expenses

    current_year_spendings = get_monthly_expenses(current_year)
    last_year_spendings = get_monthly_expenses(last_year)

    return {
        "current_year": current_year_spendings,
        "last_year": last_year_spendings,
    }


def get_yearly_comparison_by_category(
    db: Session, current_user: User, category_id: int
) -> dict:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    current_year = datetime.now().year
    last_year = current_year - 1

    current_year_spendings = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id,
            Expense.category_id == category_id,
            Expense.date >= datetime(current_year, 1, 1),
            Expense.date < datetime(current_year + 1, 1, 1),
        )
        .with_entities(func.sum(Expense.amount))
        .scalar()
    )
    last_year_spendings = (
        db.query(Expense)
        .filter(
            Expense.user_id == current_user.id,
            Expense.category_id == category_id,
            Expense.date >= datetime(last_year, 1, 1),
            Expense.date < datetime(last_year + 1, 1, 1),
        )
        .with_entities(func.sum(Expense.amount))
        .scalar()
    )

    return {
        "current_year": current_year_spendings if current_year_spendings else 0,
        "last_year": last_year_spendings if last_year_spendings else 0,
    }

def get_category_spendings(db: Session, current_user: User) -> dict:
    if current_user.role == "admin":
        raise PermissionError("Admins cannot have expenses")
    
    if current_user.is_approved == False:
        raise PermissionError("User is not approved yet")
    
    categories = db.query(Category).all()
    category_spendings = {}
    for category in categories:
        category_spendings[category.name] = (
            db.query(func.sum(Expense.amount))
            .filter(Expense.user_id == current_user.id, Expense.category_id == category.id)
            .scalar()
            or 0
        )
    return category_spendings