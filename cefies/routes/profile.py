import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from cefies.models.db.user import User
from cefies.models.forms.profile import EditProfileForm
from cefies.models.profile import ProfileData, ChangePasswordData, EditProfileData
from cefies.models.response import MessageResponse
from cefies.security import get_current_user, get_password_hash, get_hash_sha256
from cefies.internal import bucket

router = APIRouter(prefix="/profile")


@router.get("/")
def get_profile(
    user: Annotated[User, Depends(get_current_user)],
):
    return ProfileData(**user.to_dict())

@router.put("/")
async def edit_profile(
    user: Annotated[User, Depends(get_current_user)],
    form: EditProfileForm = Depends()
):
    loop = asyncio.get_running_loop()
    
    try:
        data_dict = form.to_dict()
        data_dict.pop("avatar", None)
        data = EditProfileData(**data_dict)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )
    
    user.name = data.name
    avatar_content = await form.avatar.read()
    avatar_url = await loop.run_in_executor(
        None,
        lambda: bucket.upload_file(avatar_content, get_hash_sha256(avatar_content))
    )
    user.avatar = avatar_url
    user.save()

    return MessageResponse(
        error=False,
        message="Successfully registered",
    )

@router.patch("/password")
def change_password(
    user: Annotated[User, Depends(get_current_user)],
    data: ChangePasswordData,
):
    user.password = get_password_hash(data.password)
    user.save()
    return JSONResponse(content={"detail": "password changed"}, status_code=200)
