"""Async training API router."""

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import APIRouter, Depends, status

from backend.core.config import settings
from backend.core.security import get_current_user
from backend.models.user import UserModel
from backend.schemas.train import TrainJobRequest, TrainJobResponse

router = APIRouter(prefix="/api/v1/train", tags=["Async Training"])


@router.post("", response_model=TrainJobResponse, status_code=status.HTTP_202_ACCEPTED)
@router.post("/", response_model=TrainJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_train_job(
    job_in: TrainJobRequest,
    current_user: UserModel = Depends(get_current_user),
):
    """Enqueue an asynchronous model training job to Redis ARQ queue."""
    redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)
    redis_pool = await create_pool(redis_settings)

    payload = {
        "dataset_id": job_in.dataset_id,
        "model_name": job_in.model_name,
        "hyperparameters": job_in.hyperparameters,
        "user_id": current_user.id,
    }

    job = await redis_pool.enqueue_job("simple_work", payload)

    try:
        await redis_pool.aclose()
    except AttributeError:
        await redis_pool.close()

    job_id = job.job_id if job else "unknown"

    return TrainJobResponse(
        job_id=job_id,
        status="queued",
        message="Training job successfully enqueued",
    )
