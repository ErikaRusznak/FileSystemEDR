from http.client import HTTPException

from fastapi import FastAPI, UploadFile
import aiohttp
import uvicorn
from testdb import TestDatabase
from redis import Redis

app = FastAPI()

@app.post("/scan-files_api")
async def add_file(file: UploadFile):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://beta.nimbus.bitdefender.net:443/liga-ac-labs-cloud/blackbox-scanner/',
                data={'files_api': await file.read()}) as resp:
            res = await resp.json()
            if res.status_code == 200:
                # print(res)
                db = TestDatabase()
                redis = Redis()
                await redis.insert_data(res['hash'], res['risk_level'], 600)
                await db.insert_data(res)
                return res
            else:
                raise HTTPException(500, "service unavailable")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
