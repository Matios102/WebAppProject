from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.user_schema import Token, UserRegister
from app.utils.security import get_hashed_password, verify_password
from app.utils.jwt_handler import create_access_token, decode_access_token
from app.repositories.user_repository import get_user_by_email
from app.models import User
import random
import string


def create_user(db: Session, user: UserRegister):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already registered")
    
    hashed_password = get_hashed_password(user.password)
    db_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password_hash=hashed_password,
        role="user",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def authenticate_user(db: Session, email: str, password: str) -> Optional[Token]:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("User not found")
    if not verify_password(password, user.password_hash):
        raise ValueError("Incorrect password")
    
    access_token = create_access_token(data={"sub": user.email})
    role = user.role
    return {"access_token": access_token, "role": role}


def refresh_token(db: Session, token: str) -> Optional[Token]:
    payload = decode_access_token(token)
    if not payload:
        return None

    user_email = payload.get("sub")
    user = get_user_by_email(db=db, email=user_email)
    if not user:
        return None

    new_access_token = create_access_token(data={"sub": user.email})
    return new_access_token

def check_user_approval(db: Session, user_email: str) -> bool:
    user = get_user_by_email(db, user_email)
    return user.is_approved

def get_user_role(db: Session, user_email: str) -> str:
    user = get_user_by_email(db, user_email)
    return user.role

def reset_password(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("User not found")
    password = create_password()
    user.password_hash = get_hashed_password(password)
    db.commit()
    return password


def create_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password