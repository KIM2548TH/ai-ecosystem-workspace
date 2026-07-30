"""System Health API router."""

import urllib.error
import urllib.request

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
    """Check health status of PostgreSQL, Redis, MinIO, and Label Studio services."""
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

    # Check Label Studio health
    try:
        base_url = getattr(settings, "label_studio_url", "http://localhost:8080").rstrip("/")
        health_url = f"{base_url}/health"
        try:
            req = urllib.request.Request(health_url, headers={"User-Agent": "BackendHealthCheck"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    services["label_studio"] = "healthy"
                else:
                    services["label_studio"] = f"unhealthy: HTTP status {resp.status}"
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                api_health_url = f"{base_url}/api/health"
                req_api = urllib.request.Request(api_health_url, headers={"User-Agent": "BackendHealthCheck"})
                with urllib.request.urlopen(req_api, timeout=5) as resp_api:
                    if resp_api.status == 200:
                        services["label_studio"] = "healthy"
                    else:
                        services["label_studio"] = f"unhealthy: HTTP status {resp_api.status}"
            else:
                services["label_studio"] = f"unhealthy: HTTP status {exc.code}"
    except Exception as exc:
        services["label_studio"] = f"unhealthy: {str(exc)}"

    overall_status = "healthy" if all(val == "healthy" for val in services.values()) else "degraded"

    return {
        "status": overall_status,
        "services": services,
    }

