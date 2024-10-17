from app.models import Team, User
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserBase


def get_user_by_email(db: Session, email: str) -> UserBase:
    return db.query(User).filter(User.email == email).first()    


def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, current_user: User) -> list[UserBase]:
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    if current_user.is_approved == False:
        raise PermissionError("You are not approved")
    return db.query(User).all()

def get_filtered_users(db: Session, current_user: User, status: str, email: str, name_or_surname: str, role: str) -> list[UserBase]:
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    if current_user.is_approved == False:
        raise PermissionError("You are not approved")
    
    query = db.query(User).filter(User.role != "admin")
    if status:
        query = query.filter(User.is_approved == (status.lower() == "approved"))
    if email:
        query = query.filter(User.email.contains(email))
    if name_or_surname:
        query = query.filter((User.name.contains(name_or_surname)) | (User.surname.contains(name_or_surname)))
    if role:
        query = query.filter(User.role.contains(role))
    return query.all()

def approve_user(db: Session, user_id: int, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")
    
    existing_user = get_user_by_id(db, user_id)
    if not existing_user:
        raise ValueError("User not found")

    existing_user.is_approved = True
    db.commit()
    db.refresh(existing_user)


def change_user_role(db: Session, user_id: int, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You are not an admin")

    existing_user = get_user_by_id(db, user_id)
    if not existing_user:
        raise ValueError("User not found")

    if(existing_user.role == "manager"):
        existing_user.role = "user"
    else:
        if existing_user.team_id:
            existing_team = db.query(Team).filter(Team.id == existing_user.team_id).first()
            if existing_team.manager_id:
                raise ValueError("Team already has a manager")
        existing_user.role = "manager"
    db.commit()
    db.refresh(existing_user)


def delete_user(db: Session, user_id: int, current_user: User):
    if current_user.role != "admin":
        raise PermissionError("You don't have permission to delete this user")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    db.delete(user)
    db.commit()