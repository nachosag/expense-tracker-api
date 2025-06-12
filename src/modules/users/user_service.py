from sqlmodel import select
from fastapi import HTTPException, status
from . import user_schemas
from ...database import models
from ...database.core import SessionDependency
from ..auth import auth_service
import logging


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
        request.password = auth_service.get_password_hash(request.password)
        user = models.User(**request.model_dump())
        session.add(user)
        session.commit()
        session.refresh(user)
        logging.info("Usuario registrado correctamente")
        return user
    except Exception as e:
        session.rollback()
        logging.error(e)
        raise e
