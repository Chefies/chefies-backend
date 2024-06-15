from typing import Annotated
from pydantic import BaseModel, StringConstraints


class ProfileData(BaseModel):
    email: str
    name: str
    avatar: str


class ChangePasswordData(BaseModel):
    new_password: Annotated[str, StringConstraints(min_length=8)]
    old_password: Annotated[str, StringConstraints(min_length=8)]


class EditProfileData(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1)]
