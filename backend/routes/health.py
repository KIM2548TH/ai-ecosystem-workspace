"""System Health API router."""

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import APIRouter
from sqlalchemy import text

from backend.core.config import settings
from backend.db.database import SessionLocal
from backend.services.minio_service import MinIOService

router = APIRouter(prefix="/api/v1/health", tags=["System Health"])


@router.get("")
@router.get("/")
async def check_health():
    """Check health status of PostgreSQL, Redis, and MinIO services."""
    services = {}

    # Check PostgreSQL health
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        services["postgres"] = "healthy"
    except Exception as exc:
        services["postgres"] = f"unhealthy: {str(exc)}"

    # Check Redis health
    try:
        redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)
        redis_pool = await create_pool(redis_settings)
        await redis_pool.ping()
        try:
            await redis_pool.aclose()
        except AttributeError:
            await redis_pool.close()
        services["redis"] = "healthy"
    except Exception as exc:
        services["redis"] = f"unhealthy: {str(exc)}"

    # Check MinIO health
    try:
        minio_service = MinIOService()
        minio_service.client.list_buckets()
        services["minio"] = "healthy"
    except Exception as exc:
        services["minio"] = f"unhealthy: {str(exc)}"

    overall_status = "healthy" if all(val == "healthy" for val in services.values()) else "degraded"

    return {
        "status": overall_status,
        "services": services,
    }
