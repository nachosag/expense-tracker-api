from datetime import date, datetime
import logging
from fastapi import HTTPException, status
from sqlmodel import select
from src.database.core import SessionDependency
from src.modules.auth.auth_service import AuthService
from src.modules.auth.auth_service import TokenDependency
from src.modules.expenses import expense_schema
from ...database import models


class ExpenseService:

    @staticmethod
    def validate_category_id(session: SessionDependency, category_id: int):
        category = session.exec(
            select(models.Category).where(models.Category.id == category_id)
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category_id not found"
            )

    @staticmethod
    def create(
        session: SessionDependency,
        token: TokenDependency,
        request: expense_schema.CreateExpenseRequest,
    ):
        ExpenseService.validate_category_id(session, request.category_id)
        token_data = AuthService.get_current_user(token=token)
        if not token_data.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
            )
        try:
            expense = models.Expense(**request.model_dump(), user_id=token_data.user_id)
            session.add(expense)
            session.commit()
            session.refresh(expense)
            logging.info("Expense created correctly")
            return expense
        except Exception as e:
            logging.error("An unexpected error has occurred", e)
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Unexpected error"
            )

    @staticmethod
    def get(
        session: SessionDependency,
        token: TokenDependency,
        expense_id: int,
    ):
        token_data = AuthService.get_current_user(token=token)
        stmt = select(models.Expense).where(
            models.Expense.id == expense_id, models.Expense.user_id == token_data.user_id
        )
        expense = session.exec(stmt).first()
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
        return expense

    @staticmethod
    def list(
        session: SessionDependency,
        token: TokenDependency,
        from_date: date | None,
        to_date: date | None,
    ):
        token_data = AuthService.get_current_user(token=token)
        stmt = select(models.Expense).where(models.Expense.user_id == token_data.user_id)

        if from_date:
            stmt = stmt.where(models.Expense.spent_at >= from_date)
        if to_date:
            stmt = stmt.where(models.Expense.spent_at <= to_date)

        return session.exec(stmt).all()

    @staticmethod
    def update(
        session: SessionDependency,
        token: TokenDependency,
        expense_id: int,
        request: expense_schema.UpdateExpenseRequest,
    ):
        expense = ExpenseService.get(
            session,
            token,
            expense_id,
        )

        for attr, val in request.model_dump(exclude_unset=True, exclude_none=True).items():
            if hasattr(expense, attr) and val != getattr(expense, attr):
                setattr(expense, attr, val)

        expense.updated_at = datetime.now()
        try:
            session.add(expense)
            session.commit()
            session.refresh(expense)
            logging.info("Expense updated correctly")
            return expense
        except Exception as e:
            session.rollback()
            logging.error("An unexpected error has occurred", e)
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED,
                detail="An unexpected error occurred",
            )

    @staticmethod
    def delete(
        session: SessionDependency,
        token: TokenDependency,
        expense_id: int,
    ):
        expense = ExpenseService.get(
            session,
            token,
            expense_id,
        )
        try:
            session.delete(expense)
            session.commit()
            logging.info("Expense deleted correctly")
        except Exception as e:
            session.rollback()
            logging.error("An unexpected error has occurred", e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An unexpected error occurred",
            )
