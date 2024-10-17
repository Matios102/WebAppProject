from multiprocessing.resource_tracker import getfd
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from app.utils.jwt_handler import decode_access_token
from jose import JWTError
from app.repositories.user_repository import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        if not payload:
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        user = get_user_by_email(db, email)
        if user is None:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception