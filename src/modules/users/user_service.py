from sqlmodel import select
from fastapi import HTTPException, status
from . import user_schemas
from ...database import models
from ...database.core import SessionDependency
from ..auth import auth_service


def confirm_unique_user(session: SessionDependency, request: user_schemas.UserRequest):
    if session.exec(
        select(models.User).where(models.User.email == request.email)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already register",
        )


def register_user(session: SessionDependency, request: user_schemas.UserRequest):
    try:
        confirm_unique_user(session, request)
        user_data = request.model_dump()
        user_data["password"] = auth_service.get_password_hash(user_data["password"])
        user = models.User(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        raise e
