from aioredis import Redis, create_pool

from aioworkers.core.base import AbstractEntity


class RedisPool(AbstractEntity, Redis):
    async def start(self):
        self._pool_or_conn = create_pool()
