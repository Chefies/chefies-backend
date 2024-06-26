from cefies.routes.index import router as index_router
from cefies.routes.auth import router as auth_router
from cefies.routes.profile import router as profile_router

__all__ = [
    "index_router",
    "auth_router",
    "profile_router",
]
