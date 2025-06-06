from pydantic import BaseModel


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str

    class Config:
        orm_mode = True
