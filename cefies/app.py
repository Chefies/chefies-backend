from fastapi import FastAPI

import cefies.internal.firestore  # noqa: F401 -- Intended to initialize Firebase
from cefies.routes import index_router

app = FastAPI()
app.include_router(index_router)
