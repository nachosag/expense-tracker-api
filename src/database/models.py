from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from datetime import datetime, date
from typing import Optional
from enum import StrEnum


class CategoryName(StrEnum):
    GROCERIES = "Groceries"
    LEISURE = "Leisure"
    ELECTRONICS = "Electronics"
    UTILITIES = "Utilities"
    CLOTHING = "Clothing"
    HEALTH = "Health"
    OTHERS = "Others"


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore
    id: int = Field(primary_key=True, index=True, unique=True)
    email: EmailStr = Field(index=True, nullable=False, unique=True, max_length=255)
    password: str = Field(nullable=False, max_length=255)
    name: str = Field(nullable=False, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    expenses: list["Expense"] = Relationship(back_populates="user")


class Category(SQLModel, table=True):
    __tablename__ = "categories"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: CategoryName = Field(nullable=False, max_length=50)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relación uno-a-muchos con Expense
    expenses: list["Expense"] = Relationship(back_populates="category")


class Expense(SQLModel, table=True):
    __tablename__ = "expenses"  # type: ignore
    id: int = Field(primary_key=True, index=True, unique=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    category_id: int = Field(foreign_key="categories.id", nullable=False)
    amount: float = Field(nullable=False, ge=0)
    description: Optional[str] = Field(default=None)
    spent_at: date = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relaciones inversas
    user: Optional[User] = Relationship(back_populates="expenses")
    category: Optional[Category] = Relationship(back_populates="expenses")
