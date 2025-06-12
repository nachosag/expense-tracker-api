from pydantic import BaseModel, ConfigDict


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str

    model_config = ConfigDict(from_attributes=True)
