from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
import app.repositories.user_repository as repo
from app.schemas.user_schema import UserBase
from app.utils.security import get_current_user

router = APIRouter()  

# Get filtered users based on: status, role, full name, email
@router.get("/users", response_model=list[UserBase])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: Optional[str] = Query(None, description="Filter by status (e.g., 'Approved', 'Unapproved')"),
    email: Optional[str] = Query(None, description="Search by email"),
    name_or_surname: Optional[str] = Query(None, description="Search by name or surname"),
    role: Optional[str] = Query(None, description="Filter by role (e.g., 'manager', 'user')")
):
    try:
        return repo.get_filtered_users(db, current_user, status, email, name_or_surname, role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

# Approve a user
@router.put("/users/approve/{user_id}")
def approve_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        repo.approve_user(db, user_id, current_user)
        return {"message": "User approved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
# Change user role
@router.put("/users/change-role/{user_id}")
def change_user_role(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        repo.change_user_role(db, user_id, current_user)
        return {"message": "User role changed successfully"}
    except ValueError as e:
        if "has a manager" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
# Delete a user
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        repo.delete_user(db, user_id, current_user)
        return {"message": "User deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
