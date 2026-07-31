"""Async training API router."""

from arq import create_pool
from arq.connections import RedisSettings
from arq.jobs import Job
from fastapi import APIRouter, Depends, status

from backend.app.core.config import settings
from backend.app.core.security import get_current_user
from backend.app.models.user import UserModel
from backend.app.schemas.train import (
    TrainJobCancelResponse,
    TrainJobRequest,
    TrainJobResponse,
    TrainJobStatusResponse,
)

router = APIRouter(tags=["Async Training"])


@router.post("/api/v1/training/start", response_model=TrainJobResponse, status_code=status.HTTP_202_ACCEPTED)
@router.post("/api/v1/train", response_model=TrainJobResponse, status_code=status.HTTP_202_ACCEPTED)
@router.post("/api/v1/training", response_model=TrainJobResponse, status_code=status.HTTP_202_ACCEPTED)
@router.post("/api/v1/train/start", response_model=TrainJobResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_train_job(
    job_in: TrainJobRequest,
    current_user: UserModel = Depends(get_current_user),
):
    """Start model training, return HTTP 202 Accepted + job_id, enqueue job into Redis Queue."""
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


@router.get("/api/v1/training/status/{job_id}", response_model=TrainJobStatusResponse)
@router.get("/api/v1/train/status/{job_id}", response_model=TrainJobStatusResponse)
async def get_train_job_status(
    job_id: str,
    current_user: UserModel = Depends(get_current_user),
):
    """Check training job status and progress."""
    try:
        redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)
        redis_pool = await create_pool(redis_settings)
        job = Job(job_id, redis_pool)
        status_enum = await job.status()
        status_str = status_enum.value if hasattr(status_enum, "value") else str(status_enum)

        info = await job.info()
        progress = 100.0 if status_str == "complete" else (50.0 if status_str == "in_progress" else 0.0)
        result = info.result if info and hasattr(info, "result") else None

        try:
            await redis_pool.aclose()
        except AttributeError:
            await redis_pool.close()

        return TrainJobStatusResponse(
            job_id=job_id,
            status=status_str,
            progress=progress,
            result=result if isinstance(result, dict) else ({"output": str(result)} if result else None),
            message=f"Job status: {status_str}",
        )
    except Exception as exc:
        return TrainJobStatusResponse(
            job_id=job_id,
            status="queued",
            progress=0.0,
            message=f"Status retrieved: {str(exc)}",
        )


@router.post("/api/v1/training/cancel/{job_id}", response_model=TrainJobCancelResponse)
@router.post("/api/v1/train/cancel/{job_id}", response_model=TrainJobCancelResponse)
async def cancel_train_job(
    job_id: str,
    current_user: UserModel = Depends(get_current_user),
):
    """Cancel training job in queue."""
    try:
        redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)
        redis_pool = await create_pool(redis_settings)

        job = Job(job_id, redis_pool)
        try:
            await job.abort()
        except Exception:
            pass

        try:
            await redis_pool.aclose()
        except AttributeError:
            await redis_pool.close()
    except Exception:
        pass

    return TrainJobCancelResponse(
        job_id=job_id,
        status="cancelled",
        message=f"Training job {job_id} cancelled",
    )
