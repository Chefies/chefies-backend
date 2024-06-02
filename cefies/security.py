from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from firebase_admin import auth

from cefies.models.firebase import DecodedIdToken

security = HTTPBearer()


def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    decoded_token: dict = auth.verify_id_token(token)
    return DecodedIdToken(**decoded_token)
