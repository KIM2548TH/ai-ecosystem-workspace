"""Legacy shim for train router."""

from backend.app.routers.train import (
    router,
    create_train_job,
    get_train_job_status,
    cancel_train_job,
)

__all__ = ["router", "create_train_job", "get_train_job_status", "cancel_train_job"]
