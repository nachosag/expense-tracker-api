from ...database.core import SessionDependency
from ...database import models
from . import auth_schemas
from typing import Annotated, Any
from pydantic import EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from sqlmodel import select
import logging
from .config import KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
TokenDependency = Annotated[str, Depends(oauth2_bearer)]


class AuthService:
    @staticmethod
    def _authenticate_user(email: str, password: str, session: SessionDependency):
        user = session.exec(
            select(models.User).where(models.User.email == email)
        ).first()

        if not user or not AuthService._verify_password(password, user.password):
            logging.warning("Failed authentication attempt")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        return user

    @staticmethod
    def _get_password_hash(password: str):
        return bcrypt_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str):
        return bcrypt_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(email: EmailStr, user_id: int, expires_delta: timedelta):
        claims: dict[str, Any] = {
            "sub": email,
            "id": user_id,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
        return jwt.encode(claims=claims, key=KEY, algorithm=ALGORITHM)

    @staticmethod
    def get_current_user(token: TokenDependency):
        try:
            payload = jwt.decode(token=token, key=KEY, algorithms=ALGORITHM)
            user_id = payload.get("id")
            return auth_schemas.TokenData(user_id=user_id)
        except JWTError as e:
            logging.warning(f"Token verification failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

    @staticmethod
    def _confirm_unique_user(
        session: SessionDependency, request: auth_schemas.SignupRequest
    ):
        stmt = select(models.User).where(models.User.email == request.email)
        if session.exec(stmt).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already register",
            )

    @staticmethod
    def login(
        session: SessionDependency,
        form_data: OAuth2PasswordRequestForm,
    ):
        user = AuthService._authenticate_user(
            form_data.username, form_data.password, session
        )
        token = AuthService.create_access_token(
            user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return auth_schemas.Token(access_token=token, token_type="bearer")

    @staticmethod
    def signup(session: SessionDependency, request: auth_schemas.SignupRequest):
        try:
            AuthService._confirm_unique_user(session, request)
            request.password = AuthService._get_password_hash(request.password)
            user = models.User(**request.model_dump())
            session.add(user)
            session.commit()
            session.refresh(user)
            logging.info("User registered correctly")
            return user
        except HTTPException:
            session.rollback()
            raise
        except Exception as e:
            session.rollback()
            logging.error("An unexpected error occurred", e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An unexpected error occurred",
            )
