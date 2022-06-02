import asyncio
import aioredis


async def main():
    redis = aioredis.from_url("redis://localhost")

    # await redis.set("o_cheie", "value")
    # value = await redis.get("o_cheie")
    # for i in range(10):
    #    await redis.lpush("listamea", f"val{i}")
    # elements = await redis.lrange("listamea", 0, 3)

    await redis.hset("md5123", mapping={"key1": "val1", "key2":"val2"})
    await redis.expire("md5123", 15)
    await redis.close()
    # print(elements)

    await redis.close()

if __name__ == '__main__':
    asyncio.run(main())