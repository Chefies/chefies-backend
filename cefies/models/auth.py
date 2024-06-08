from typing import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints


class Token(BaseModel):
    token: str


class LoginData(BaseModel):
    email: EmailStr
    password: str


class RegisterData(BaseModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8)]
    name: Annotated[str, StringConstraints(min_length=1)]
