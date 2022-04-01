import logging

from fastapi import Depends, APIRouter, HTTPException, status
from aioredis import Redis
from aioredis.exceptions import ConnectionError

from app.api.dependencies.redis import get_redis

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", name="system:health")
async def healthcheck_service():
    return {"status": "alive"}


@router.get("/health/redis", name="system:health-redis")
async def healthcheck_service_redis(redis: Redis = Depends(get_redis)):
    try:
        await redis.ping()
    except ConnectionError as conn_exc:
        logger.exception(conn_exc)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return {"status": "alive"}
