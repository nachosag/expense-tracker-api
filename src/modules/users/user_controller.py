from fastapi import APIRouter, status

from src.database.core import SessionDependency
from . import user_schemas, user_service

users_router = APIRouter()


@users_router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
    response_model=user_schemas.UserResponse,
)
async def register_user(session: SessionDependency, request: user_schemas.UserRequest):
    return user_service.register_user(session, request)
