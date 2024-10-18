from sqlalchemy.orm import Session
from app.models import Category, Expense, User


def get_categories_for_admin(
    db: Session, current_user: User, ascending: bool, name: str
) -> list[dict]:
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")

    categories = db.query(Category)

    if name:
        categories = categories.filter(Category.name.contains(name))
    category_info = []
    for category in categories:
        expense_count = (
            db.query(Expense).filter(Expense.category_id == category.id).count()
        )
        category_info.append(
            {"id": category.id, "name": category.name, "expense_count": expense_count}
        )
    if ascending:
        category_info.sort(key=lambda x: x["expense_count"])
    else:
        category_info.sort(key=lambda x: x["expense_count"], reverse=True)

    return category_info

def get_categories(db: Session, current_user: User) -> list[dict]:
    if(current_user.is_approved == False):
        raise PermissionError("You are not approved")
    
    categories = db.query(Category).all()
    return categories


def create_category(db: Session, name: str, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        raise ValueError("Category already exists")
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)


def delete_category(db: Session, category_id: int, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )
    if category is None:
        raise ValueError("Category not found")
    if category.name == "default":
        raise ValueError("Cannot delete default category")

    expenses_with_deleted_category = (
        db.query(Expense).filter(Expense.category_id == category_id).all()
    )
    for expense in expenses_with_deleted_category:
        expense.category_id = 1
    db.delete(category)
    db.commit()


def update_category(db: Session, category_id: int, name: str, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.name != "default")
        .first()
    )
    if category is None:
        raise ValueError("Category not found")
    
    existing_category = db.query(Category).filter(Category.name == name).first()
    if existing_category:
        raise ValueError("Category already exists")

    category.name = name
    db.commit()
    db.refresh(category)
