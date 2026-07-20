"""Script to enqueue background jobs into the Redis ARQ queue."""

import asyncio
import sys
from pathlib import Path
from typing import Any, Dict

# Ensure root directory is in sys.path when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from arq import create_pool
from arq.connections import RedisSettings

from backend.core.config import settings


async def enqueue_simple_job() -> None:
    """Enqueue a job to the Redis ARQ queue with error handling and status output."""
    redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)

    print(f"[Info] Connecting to Redis at {settings.redis_host}:{settings.redis_port}...")
    try:
        redis_pool = await create_pool(redis_settings)
        payload: Dict[str, Any] = {
            "msg": "Hello from ARQ Queue",
            "task": "Async Job Execution",
        }
        job = await redis_pool.enqueue_job("simple_work", payload)
        print("[Success] Job successfully enqueued to Redis ARQ queue!")
        print(f"  - Job ID: {job.job_id if job else 'Unknown'}")
        print("  - Payload parameters:")
        for key, val in payload.items():
            print(f"      * {key}: {val}")
        try:
            await redis_pool.aclose()
        except AttributeError:
            await redis_pool.close()
    except Exception as exc:
        print(f"[Error] Failed to enqueue job into Redis ARQ queue: {exc}")
        raise


def main() -> None:
    """Main execution entrypoint."""
    asyncio.run(enqueue_simple_job())


if __name__ == "__main__":
    main()

