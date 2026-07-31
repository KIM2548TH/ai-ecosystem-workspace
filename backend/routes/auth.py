"""Legacy shim for auth router."""

from backend.app.routers.auth import router, register, login, get_me

__all__ = ["router", "register", "login", "get_me"]
