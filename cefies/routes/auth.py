from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import ValidationError

from cefies.models.forms.auth import RegisterForm
from cefies.models.auth import LoginData, RegisterData, Token
from cefies.models.db.user import User
from cefies.models.response import MessageResponse
from cefies.security import authenticate_user, create_access_token, get_password_hash, get_hash_sha256
from cefies.internal import bucket


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
async def register(form: RegisterForm = Depends()):
    try:
        data_dict = form.to_dict()
        data_dict.pop("avatar", None)
        data = RegisterData(**data_dict)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )
    
    existing_user = User.collection.filter(email=data.email).get()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email has been used",
        )

    new_user = User()
    new_user.email = data.email
    new_user.name = data.name
    new_user.password = get_password_hash(data.password)
    avatar_content = await form.avatar.read()
    avatar_url = bucket.upload_file(avatar_content, get_hash_sha256(avatar_content))
    new_user.avatar = avatar_url
    new_user.save()

    return MessageResponse(
        error=False,
        message="Successfully registered",
    )
