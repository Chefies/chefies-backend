from fastapi import FastAPI

import cefies.internal.firestore  # noqa: F401 -- Intended to initialize Firebase
from cefies.routes import index_router, auth_router, profile_router

app = FastAPI(root_path="/api")
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(profile_router)
