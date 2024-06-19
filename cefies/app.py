import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

import cefies.internal.firestore  # noqa: F401 -- Intended to initialize Firebase
from cefies.routes import index_router, auth_router, profile_router

root_path = ""
if os.getenv("PRODUCTION"):
    root_path = "/api"

app = FastAPI(root_path=root_path)
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(profile_router)
