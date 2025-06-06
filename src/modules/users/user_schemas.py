from pydantic import BaseModel, EmailStr
from ..expenses import expense_schema


class UserRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    expenses: list[expense_schema.ExpenseResponse] = []

    class Config:
        orm_mode = True
