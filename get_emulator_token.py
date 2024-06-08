import os
from typing import cast
from firebase_admin import auth
import httpx
from cefies.internal.firestore import app

API_KEY = os.getenv("API_KEY", "")

try:
    user = auth.get_user_by_email(email="example@example.com")
except:
    user: auth.UserRecord = auth.create_user(email="example@example.com", password="sample")

custom_token = auth.create_custom_token(user.uid).decode()
response = httpx.post(
    "http://localhost:9099/www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key=" + API_KEY,
    json={"token": custom_token, "returnSecureToken": True},
)


print(response.json())
