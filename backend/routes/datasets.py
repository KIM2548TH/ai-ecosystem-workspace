"""Legacy shim for datasets router."""

from backend.app.routers.datasets import router, upload_dataset, get_datasets, get_dataset_by_id

__all__ = ["router", "upload_dataset", "get_datasets", "get_dataset_by_id"]
