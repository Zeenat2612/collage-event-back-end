from app.routers.auth import router as auth_router
from app.routers.events import router as events_router
from app.routers.registrations import router as registrations_router
from app.routers.users import router as users_router
from app.routers.analytics import router as analytics_router
from app.routers.notifications import router as notifications_router

__all__ = [
    "auth_router",
    "events_router",
    "registrations_router",
    "users_router",
    "analytics_router",
    "notifications_router"
]
