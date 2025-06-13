from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ExpenseBase(BaseModel):
    category_id: int
    amount: float = Field(gt=0)
    description: Optional[str]
    spent_at: date


class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateExpenseRequest(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)


class UpdateExpenseRequest(BaseModel):
    category_id: Optional[int]
    amount: Optional[float] = Field(gt=0)
    description: Optional[str]
    spent_at: Optional[date]
