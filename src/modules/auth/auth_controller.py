from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ...database.core import SessionDependency
from . import auth_service, auth_schemas, config

auth_router = APIRouter()


@auth_router.post(
    "/login", response_model=auth_schemas.Token, status_code=status.HTTP_200_OK
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: SessionDependency = Depends(),
):
    user = auth_service.authenticate_user(
        form_data.username, form_data.password, session
    )
    token = auth_service.create_access_token(
        user.email, user.id, timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return auth_schemas.Token(access_token=token, token_type="bearer")
