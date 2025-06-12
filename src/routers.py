from fastapi import FastAPI
from .modules.auth.auth_controller import auth_router

# from .modules.expenses.expense_controller


def add_routers(app: FastAPI):
    app.include_router(auth_router, tags=["AUTH"], prefix="/auth")
