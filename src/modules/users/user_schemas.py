from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
