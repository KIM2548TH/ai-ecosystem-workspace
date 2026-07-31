"""Legacy shim for config module."""

from backend.app.core.config import Settings, settings, ENV_FILE, ROOT_DIR

__all__ = ["Settings", "settings", "ENV_FILE", "ROOT_DIR"]
