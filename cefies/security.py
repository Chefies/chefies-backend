from http.client import UNAUTHORIZED
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from firebase_admin import auth

from cefies.models.firebase import DecodedIdToken

security = HTTPBearer()


def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        decoded_token: dict = auth.verify_id_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=UNAUTHORIZED, detail="Invalid token")

    return DecodedIdToken(**decoded_token)
