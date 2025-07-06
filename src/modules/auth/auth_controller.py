from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ...database.core import SessionDependency
from . import auth_schemas
from .auth_service import AuthService

auth_router = APIRouter()


@auth_router.post(
    path="/login", response_model=auth_schemas.Token, status_code=status.HTTP_200_OK
)
def login(
    session: SessionDependency,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return AuthService.login(session, form_data)

@auth_router.post(
    path="/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=auth_schemas.SignupResponse,
)
def signup(session: SessionDependency, request: auth_schemas.SignupRequest):
    return AuthService.signup(session, request)
