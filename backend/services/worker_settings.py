"""ARQ Worker configuration and background task definitions."""

import sys
from pathlib import Path
from typing import Any, Dict

# Ensure root directory is in sys.path when running worker directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from arq.connections import RedisSettings

from backend.core.config import settings


async def simple_work(ctx: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """Async background task for ARQ worker queue processing."""
    print("[Worker] Processing job...")
    if isinstance(data, dict):
        for key, val in data.items():
            print(f"  - {key}: {val}")
    else:
        print(f"  - Payload: {data}")
    return {"status": "done", "data": data}


class WorkerSettings:
    """ARQ Worker configuration settings."""

    functions = [simple_work]
    redis_settings: RedisSettings = RedisSettings(
        host=settings.redis_host,
        port=settings.redis_port,
    )

