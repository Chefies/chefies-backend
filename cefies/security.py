import os
from typing import Annotated, cast
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import bcrypt

from cefies.models.db.user import User
from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = os.getenv("SECRET_KEY", "insecurekey000000000000000000000")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = OAuth2PasswordBearer("/auth/login")


def authenticate_user(email: str, password: str):
    user: User | None = User.collection.filter(email=email).get()
    if not user:
        return None

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        return None

    return cast(User, user)


def create_access_token(user_id: str, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire = datetime.now(timezone.utc) + expires_delta
    encoded_jwt = jwt.encode(
        {
            "sub": user_id,
            "exp": expire,
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def get_current_user(token: Annotated[str, Depends(security)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = User.collection.get(user_id)
    if not user:
        raise credentials_exception

    return cast(User, user)
