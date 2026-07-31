"""Legacy shim for inference router."""

from backend.app.routers.inference import router, predict

__all__ = ["router", "predict"]
