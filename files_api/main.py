from fastapi import FastAPI, UploadFile
import aiohttp
import uvicorn
from test import TestDatabase
app = FastAPI()

@app.post("/scan-files_api")
async def add_file(file: UploadFile):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://beta.nimbus.bitdefender.net:443/liga-ac-labs-cloud/blackbox-scanner/',
                data={'files_api': await file.read()}) as resp:
            res = await resp.json()
            db = TestDatabase()
            await db.insert_data(res)
            return res

if __name__ == '__main__':
    uvicorn.run(app, port=8001)
