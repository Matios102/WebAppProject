from database import Base
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=True) #user, manager, admin 
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)
    is_approved = Column(Boolean, nullable=False, default=False)

"""
Role descritpion:
- user: view, create, update and delete own expenses -> personalized categories colors
- manager: view team expenses, view, create, update and delete own expenses
- admin: change user role, approve user, create teams
"""

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    manager_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
 
class Income(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False) 
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

class SpendingGoal(Base):
    __tablename__ = 'spending_goals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Float, nullable=False)
    Category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)