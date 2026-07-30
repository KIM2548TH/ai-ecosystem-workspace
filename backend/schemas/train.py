"""Schemas for training jobs."""

from typing import Any, Dict, Optional
from pydantic import BaseModel


class TrainJobRequest(BaseModel):
    """Training job request schema."""

    dataset_id: int
    model_name: str
    hyperparameters: Optional[Dict[str, Any]] = None


class TrainJobResponse(BaseModel):
    """Training job response schema."""

    job_id: str
    status: str = "queued"
    message: str
