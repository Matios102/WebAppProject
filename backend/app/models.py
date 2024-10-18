from app.database import Base
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Date


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=True)  # user, manager, admin
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    is_approved = Column(Boolean, nullable=False, default=False)


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    manager_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )


class Expense(Base): 
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
