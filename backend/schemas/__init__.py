"""Legacy shim for schemas package."""

from backend.app.schemas import auth, dataset, inference, model, train

__all__ = ["auth", "dataset", "inference", "model", "train"]
