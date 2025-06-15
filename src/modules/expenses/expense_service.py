import logging
from fastapi import HTTPException, status
from sqlmodel import select
from src.database.core import SessionDependency
from src.modules.auth import auth_service
from src.modules.auth.auth_service import TokenDependency
from src.modules.expenses import expense_schema
from ...database import models


def validate_category_id(session: SessionDependency, category_id: int):
    category = session.exec(
        select(models.Category).where(models.Category.id == category_id)
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category_id not found"
        )


def create_expense(
    session: SessionDependency,
    token: TokenDependency,
    request: expense_schema.CreateExpenseRequest,
):
    validate_category_id(session, request.category_id)
    token_data = auth_service.get_current_user(token=token)
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    try:
        expense = models.Expense(**request.model_dump(), user_id=token_data.user_id)
        session.add(expense)
        session.commit()
        session.refresh(expense)
        return expense
    except Exception as e:
        logging.error(e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error"
        )


def get_expense(expense_id: int, session: SessionDependency, token: TokenDependency):
    token_data = auth_service.get_current_user(token=token)
    stmt = select(models.Expense).where(
        models.Expense.id == expense_id, models.Expense.user_id == token_data.user_id
    )
    expense = session.exec(stmt).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
        )
    return expense

def list_expenses(session: SessionDependency, token: TokenDependency):
    token_data = auth_service.get_current_user(token=token)
    stmt = select(models.Expense).where(
        models.Expense.user_id == token_data.user_id
    )
    return session.exec(stmt).all()