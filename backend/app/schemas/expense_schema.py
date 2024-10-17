from datetime import date
import datetime
from typing import Optional
from pydantic import BaseModel

class ExpenseBase(BaseModel):
    id: int
    name: str
    amount: float
    date: date
    category_id: int
    user_id: int

class ExpenseList(BaseModel):
    id: int
    name: str
    amount: float
    date: date
    category_name: str
    category_id: int

class ExpenseView(BaseModel):
    name: str
    amount: float
    date: date
    category_name: str

class ExpenseCreate(BaseModel):
    name: str
    amount: float
    date: date
    category_id: Optional[int] = None

class ExpenseUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime.date] = None
    category_id: Optional[int] = None