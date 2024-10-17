from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.utils.security import get_current_user
import app.repositories.expenses_repository as repo
from app.schemas.expense_schema import ExpenseCreate, ExpenseUpdate


router = APIRouter()


# List all expenses of the current user
@router.get("/expenses")
def get_expenses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
    expense_name: Optional[str] = Query(None, description="Search by name"),
    expense_amount: Optional[float] = Query(None, description="Search by amount"),
    expense_category: Optional[int] = Query(None, description="Search by category"),
    expense_date: Optional[date] = Query(None, description="Search by date"),
):
    try:
        return repo.get_expenses(db, current_user, expense_name, expense_amount, expense_category, expense_date)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


# Create a new expense
@router.post("/expenses")
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.create_expense(db, expense, current_user)
        return {"message": "Expense created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


# Update an existing expense
@router.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return repo.update_expense(db, expense_id, expense, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


# Delete an existing expense
@router.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.delete_expense(db, expense_id, current_user)
        return {"message": "Expense deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


# Get total spendings of the current user
@router.get("/expenses/statistics/total-spendings")
def get_total_spendings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return repo.get_total_spendings(db, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Get yearly comparison of the current user
@router.get("/expenses/statistics/yearly-comparison")
def get_yearly_comparison(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return repo.get_yearly_comparison(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

# Get category spendings of the current user
@router.get("/expenses/statistics/category-spendings")
def get_category_spendings(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return repo.get_category_spendings(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
