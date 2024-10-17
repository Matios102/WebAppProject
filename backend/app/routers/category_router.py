from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.security import get_current_user
from app.models import User
import app.repositories.category_repository as repo

router = APIRouter()


# List all the categories
@router.get("/admin/categories")
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ascending: Optional[bool] = Query(True, description="Filter by ascending t/f"),
    name: Optional[str] = Query(None, description="Search by name"),
):
    try:
        return repo.get_categories_for_admin(db, current_user, ascending, name)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


# For everyone lis all the categories
@router.get("/categories")
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return repo.get_categories(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


# Create a new category
@router.post("/categories")
def create_category(
    category_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.create_category(db, category_name, current_user)
        return {"message": "Category created"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


# Update an existing category
@router.put("/categories/{category_id}")
def update_category(
    category_id: int,
    category_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.update_category(db, category_id, category_name, current_user)
        return {"message": "Category updated"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        if "exists" in str(e):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


# Delete an existing category
@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.delete_category(db, category_id, current_user)
        return {"message": "Category deleted"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
