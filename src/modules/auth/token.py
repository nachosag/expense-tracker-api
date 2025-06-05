from jose import jwt, JWTError
from typing import Annotated, Any, Dict
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

KEY: str = os.environ.get("KEY") or ""
ALGORITHM: str = os.environ.get("ALGORITHM") or ""
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

if not KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise RuntimeError(
        "KEY, ALGORITHM, or ACCESS_TOKEN_EXPIRE_MINUTES env vars are not set"
    )

try:
    TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
except (TypeError, ValueError):
    raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be an integer")


def encode_token(payload: Dict[str, Any]) -> str:
    """
    Codifica un payload en un JWT con expiración.
    """
    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload_with_exp = payload.copy()
    payload_with_exp["exp"] = int(expire.timestamp())
    return jwt.encode(payload_with_exp, key=KEY, algorithm=ALGORITHM)


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Dict[str, Any]:
    """
    Decodifica un JWT y retorna el payload.
    Lanza HTTPException si el token es inválido.
    """
    try:
        data = jwt.decode(
            token=token,
            key=KEY,
            algorithms=[ALGORITHM],
        )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


TokenDependency = Annotated[Dict[str, Any], Depends(decode_token)]
