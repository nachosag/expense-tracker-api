from datetime import date
from . import expense_schema
from .expense_service import ExpenseService
from ...database.core import SessionDependency
from ..auth.auth_service import TokenDependency
from fastapi import APIRouter, status

expenses_router = APIRouter()


@expenses_router.post(
    path="/",
    response_model=expense_schema.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    session: SessionDependency,
    token: TokenDependency,
    request: expense_schema.CreateExpenseRequest,
):
    return ExpenseService.create(session, token, request)

@expenses_router.get(
    path="/",
    response_model=list[expense_schema.ExpenseResponse],
    status_code=status.HTTP_200_OK,
)
def list_expenses(
    session: SessionDependency,
    token: TokenDependency,
    from_date: date | None = None,
    to_date: date | None = None,
):
    return ExpenseService.list(
        session,
        token,
        from_date,
        to_date,
    )

@expenses_router.get(
    path="/{expense_id}",
    response_model=expense_schema.ExpenseResponse,
    status_code=status.HTTP_200_OK,
)
def get_expense(
    session: SessionDependency,
    token: TokenDependency,
    expense_id: int,
):
    return ExpenseService.get(session, token, expense_id)

@expenses_router.patch(
    path="/{expense_id}",
    response_model=expense_schema.ExpenseResponse,
    status_code=status.HTTP_200_OK,
)
def update_expense(
    session: SessionDependency,
    token: TokenDependency,
    expense_id: int,
    request: expense_schema.UpdateExpenseRequest,
):
    return ExpenseService.update(session, token, expense_id, request)

@expenses_router.delete(
    path="/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(expense_id: int, session: SessionDependency, token: TokenDependency):
    return ExpenseService.delete(session, token, expense_id)