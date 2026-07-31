"""Legacy shim for routes package initialization."""

from backend.app.routers import auth, datasets, health, inference, models, train

__all__ = ["auth", "datasets", "health", "inference", "models", "train"]
