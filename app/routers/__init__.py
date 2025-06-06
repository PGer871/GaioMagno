from .frontend import router as frontend_router
from .events import router as events_router
from .users import router as users_router
from .registrations import router as registrations_router

__all__ = [
    "frontend_router",
    "events_router",
    "users_router",
    "registrations_router",
]
