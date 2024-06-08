from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, status

from cefies.models.auth import LoginData, RegisterData, Token
from cefies.models.db.user import User
from cefies.models.response import MessageResponse
from cefies.security import authenticate_user, create_access_token, get_password_hash


router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(data: LoginData):
    user = authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.key)
    return Token(token=token)


@router.post("/register")
def register(data: RegisterData):
    existing_user = User.collection.filter(email=data.email).get()
    print(existing_user)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email has been used",
        )

    new_user = User()
    new_user.email = data.email
    new_user.name = data.name
    new_user.password = get_password_hash(data.password)
    # TODO: Upload file to object and set avatar
    new_user.avatar = ""
    new_user.save()

    return MessageResponse(
        error=False,
        message="Successfully registered",
    )
