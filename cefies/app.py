from fastapi import FastAPI

from cefies.routes import index_router

app = FastAPI()
app.include_router(index_router)
