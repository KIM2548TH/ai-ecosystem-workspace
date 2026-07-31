"""Legacy shim for health router."""

from backend.app.routers.health import router, check_health, get_system_logs

__all__ = ["router", "check_health", "get_system_logs"]
