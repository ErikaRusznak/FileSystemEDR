import pprint
import random
import motor.motor_asyncio

# using motor with asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://db:27017')
db = client['test_db']


async def do_insert():
    document = {'value': 'test' + str(random.randint(0, 100)), 'i': random.randint(0,7)}
    result = await db.test_collection.insert_one(document)
    print('result %s' % repr(result.inserted_id))


async def do_find_one():
    document = await db.test_collection.find_one({'i': {'$lt': 1}})
    pprint.pprint(document)


async def do_find():
    cursor = db.test_collection.find({'i': {'$lt': 5}}).sort('i')
    for document in await cursor.to_list(length=100):
        pprint.pprint(document)


async def main():
    await do_insert()
    print('find_one()')
    await do_find_one()
    print('find() many')
    await do_find()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
