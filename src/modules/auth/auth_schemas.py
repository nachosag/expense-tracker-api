from pydantic import BaseModel, EmailStr, ConfigDict
from ..expenses import expense_schema


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class SignupResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    expenses: list[expense_schema.ExpenseResponse] = []

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None
