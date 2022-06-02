import asyncio
import os

import aioredis

class Redis:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = aioredis.from_url(redis_url)

    async def insert_data(self, key, data, expire=None):
        await self.client.set(name=key, value=data, keepttl=expire)

    async def find_data(self, key):
        return await self.client.get(name=key)

