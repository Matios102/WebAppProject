from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from utils.security import get_current_user
from models import User
import repositories.team_repository as repo

router = APIRouter()


# For manager list all team members
@router.get("/team")
def get_team(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return repo.get_team(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
 
# For Admin list all teams
@router.get("/team/all")
def get_all_teams(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return repo.get_all_teams(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
# For Admin list all users without a team
@router.get("/team/users") 
def get_users_without_team(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
    name_or_surname: Optional[str] = Query(None, description="Search by name or surname"),
):
    try:
        return repo.get_users_without_team(db, current_user, name_or_surname)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

# For Admin create a new team
@router.post("/team/create")
def create_team(
    team_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.create_team(db, team_name, current_user)
        return {"message": "Team created"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

# For Admin delete a team
@router.delete("/team/delete")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.delete_team(db, team_id, current_user)
        return {"message": "Team deleted"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


# For Admin add a new team member
@router.post("/team")
def add_team_member(
    user_id: int,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.add_team_member(db, user_id, team_id, current_user)
        return {"message": "User added to the team"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")


# For Admin delete a team member
@router.delete("/team")
def delete_team_member(
    user_id: int,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        repo.delete_team_member(db, user_id, team_id,current_user)
        return {"message": "User removed from the team"}
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

# For Manager get team expenses
@router.get("/team/expenses")
def get_team_expenses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return repo.get_team_expenses(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# For Manager get team expenses by category
@router.get("/team/expenses/by-category")
def get_team_expenses_by_category(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return repo.get_team_expenses_by_category(db, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
