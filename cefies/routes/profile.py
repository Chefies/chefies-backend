from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from cefies.models.db.user import User
from cefies.models.profile import ProfileData, ChangePasswordData
from cefies.security import get_current_user, get_password_hash


router = APIRouter(prefix="/profile")


@router.get("/")
def get_profile(
    user: Annotated[User, Depends(get_current_user)],
):
    return ProfileData(**user.to_dict())

@router.patch("/password")
def change_password(
    user: Annotated[User, Depends(get_current_user)],
    data: ChangePasswordData,
):
    user.password = get_password_hash(data.password)
    user.save()
    return JSONResponse(content={"detail": "password changed"}, status_code=200)
