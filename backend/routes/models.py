"""Legacy shim for models router."""

from backend.app.routers.models import (
    router,
    register_or_upload_model,
    get_models,
    get_latest_model,
    get_model_by_id,
)

__all__ = [
    "router",
    "register_or_upload_model",
    "get_models",
    "get_latest_model",
    "get_model_by_id",
]
