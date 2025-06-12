from fastapi import FastAPI
from .modules.auth.auth_controller import auth_router
from .modules.expenses.expense_controller import expenses_router


def add_routers(app: FastAPI):
    app.include_router(auth_router, tags=["AUTH"], prefix="/auth")
    app.include_router(expenses_router, tags=["EXPENSES"], prefix="/expenses")
