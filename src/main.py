from fastapi import FastAPI
from src.database.core import lifespan
from .routers import add_routers

app = FastAPI(
    title="Expense Tracker RESTful API",
    lifespan=lifespan,
    root_path="/api/v1",
    version="0.1.0",
)

add_routers(app)
