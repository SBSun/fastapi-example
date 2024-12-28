from dataclasses import dataclass
from datetime import timedelta, datetime, timezone
from enum import StrEnum
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette.status import HTTP_403_FORBIDDEN

from config import get_settings

settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")

class Role(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"

@dataclass
class CurrentUser:
    id: str
    role: Role

def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")

    if not user_id or not role or role != Role.USER:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)

    return CurrentUser(user_id, Role(role))

def get_admin_user(token: Annotated[str, Depends(oauth2_schema)]):
    payload = decode_access_token(token)

    role = payload.get("role")
    # if not role or role != Role.ADMIN:
    if not role:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)

    return CurrentUser("ADMIN_USER_ID", role)

def create_access_token(
    payload: dict,
    role: Role,
    expires_delta: timedelta = timedelta(hours=6)
):
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update(
        {
            "role": role,
            "exp": expire
        }
    )
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)