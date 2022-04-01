import logging

from app.core.config import redis_pool

logger = logging.getLogger(__name__)


async def connect_to_redis():
    logger.info("Connect to redis")
    await redis_pool.connect()


async def disconnect_from_redis():
    logger.info("Disconnect from redis")
    await redis_pool.disconnect()
