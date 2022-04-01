from aioredis import Redis, from_url


class RedisPool:
    """
    Helper class to manage Redis connections.
    """

    def __init__(self, uri: str):
        self.uri = uri
        self._pool: Redis | None = None

    @property
    def is_closed(self) -> bool:
        """
        Check if redis pool is closed
        """
        return not self._pool

    async def connect(self) -> None:
        """
        Connect to redis
        """
        if self.is_closed:
            self._pool = from_url(self.uri, encoding="utf-8", decode_responses=True)

    async def disconnect(self) -> None:
        """
        Disconnect from redis
        """
        if not self.is_closed:
            await self._pool.close()

    @property
    def redis(self) -> Redis:
        """
        Get redis instance
        :return: Redis instance
        """
        if self.is_closed:
            raise RuntimeError("Redis pool is closed")

        return self._pool
