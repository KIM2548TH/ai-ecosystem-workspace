"""Legacy shim for models package."""

from backend.app.models import Base, DatasetModel, ModelRegistryModel, UserModel

__all__ = ["Base", "UserModel", "DatasetModel", "ModelRegistryModel"]
