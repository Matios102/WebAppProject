from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserRegister, Token, TokenRequest
from app.repositories.user_repository import get_user_by_email
import app.repositories.auth_repository as repo

router = APIRouter()


# Register a new user
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
        try:
            repo.create_user(db, user)
            return {"message": "User created successfully"}
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Login and get an access token
@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    try:
        user_data = repo.authenticate_user(db, form_data.username, form_data.password)
        return {"access_token": user_data["access_token"], "role": user_data["role"] ,"token_type": "bearer"}
    except ValueError as e:
        if str(e) == "User not found":
            raise HTTPException(status_code=404, detail="User not found")
        elif str(e) == "Incorrect password":
            raise HTTPException(status_code=401, detail="Incorrect password")
    

# Reset password
@router.post("/reset-password")
def reset_password(email: str, db: Session = Depends(get_db)):
    try:
        password = repo.reset_password(db, email)
        return {"password": password}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Check if a token is valid
@router.post("/check-token")
def check_token(token: TokenRequest, db: Session = Depends(get_db)):
    payload = repo.decode_access_token(token.token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    is_approved = repo.check_user_approval(db, payload["sub"])
    role = repo.get_user_role(db, payload["sub"])

    return {"role": role, "is_approved": is_approved}


# Refresh an access token
@router.post("/refresh-token")
def refresh_token(token: str, db: Session = Depends(get_db)):
    new_access_token = repo.refresh_token(db, token)
    if not new_access_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"access_token": new_access_token, "token_type": "bearer"}
