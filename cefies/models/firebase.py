from pydantic import BaseModel
from typing import Any, Dict


# Converted from https://github.com/firebase/firebase-admin-node/blob/master/src/auth/token-verifier.ts#L35
class _Firebase(BaseModel):
    identities: Dict[str, Any]
    sign_in_provider: str
    sign_in_second_factor: str | None = None
    second_factor_identifier: str | None = None
    tenant: str | None = None

    class Config:
        extra = "allow"


class DecodedIdToken(BaseModel):
    aud: str
    auth_time: int
    email: str | None = None
    email_verified: bool | None = None
    exp: int
    firebase: _Firebase
    iat: int
    iss: str
    phone_number: str | None = None
    picture: str | None = None
    sub: str
    uid: str

    class Config:
        extra = "allow"
