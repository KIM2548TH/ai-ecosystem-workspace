"""Legacy shim for worker_settings module."""

from backend.app.services.worker_settings import WorkerSettings, simple_work

__all__ = ["WorkerSettings", "simple_work"]
