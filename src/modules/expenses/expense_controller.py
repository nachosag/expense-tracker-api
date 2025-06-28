from . import expense_schema, expense_service
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
    return expense_service.create_expense(session, token, request)


@expenses_router.get(
    path="/",
    response_model=list[expense_schema.ExpenseResponse],
    status_code=status.HTTP_200_OK,
)
def list_expenses(session: SessionDependency, token: TokenDependency):
    return expense_service.list_expenses(session, token)


@expenses_router.get(
    path="/{expense_id}",
    response_model=expense_schema.ExpenseResponse,
    status_code=status.HTTP_200_OK,
)
def get_expense(expense_id: int, session: SessionDependency, token: TokenDependency):
    return expense_service.get_expense(expense_id, session, token)


@expenses_router.patch(
    path="/{expense_id}",
    response_model=expense_schema.ExpenseResponse,
    status_code=status.HTTP_200_OK,
)
def update_expense(
    expense_id: int,
    request: expense_schema.UpdateExpenseRequest,
    session: SessionDependency,
    token: TokenDependency,
):
    return expense_service.update_expense(expense_id, request, session, token)


@expenses_router.delete(
    path="/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(expense_id: int, session: SessionDependency, token: TokenDependency):
    pass
