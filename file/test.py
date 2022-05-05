import asyncio
import os

import motor.motor_asyncio

class TestDatabase:

    def __init__(self):
        try:
            mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
            self._client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
            self._collection = self._client.files_db.Erika
        except Exception as e:
            raise Exception("failed to init database because " + e)

    async def insert_data(self, data):
        await self._collection.insert_one(dict(data))

    async def find_data(self, some_key):
        retval = await self._collection.find_one({"hash": some_key})
        # print(type(retval))
        return retval


async def main():
    try:
        db = TestDatabase()
        await db.insert_data({"hash": "abc123", "other":12})
        doc = await db.find_data("cba123")
        print(f"f1:{doc}")
        doc = await db.find_data("abc123")
        print(f"f2:{doc}")
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())