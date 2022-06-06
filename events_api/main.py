import sys, os

from prometheus_fastapi_instrumentator import Instrumentator

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from event_model import Event
from files_api.testdb import TestDatabase
from files_api.redis import Redis
from response_model import Response, BaseResponse
import uvicorn
from fastapi import FastAPI
import json
import sys
from prometheus_fastapi_instrumentator import Instrumentator

sys.path.append('../files_api/')

app = FastAPI()

# http_request_count_total = 0

@app.get("/")
async def root():
    return {'title': 'File System Edr'}


# redis bloom filter:
    # pentru chestii pe care iti zice true: este o sansa sa nu fie de fapt
    # pentru chestii pe care iti zice fals: sigur nu exista


# @app.get("/metrics")
# async def metrics():
#    return f"http_request_count_total {http_request_count_total}"


@app.post("/events", response_model=Response)
async def add_event(event: Event) -> Response:
    
    # http_request_count_total += 1
    db = TestDatabase()
    # redis stuff
    redis = Redis()
    risk = await redis.find_data(event.file.file_hash)

    if risk is None:
        risk = await db.find_data(event.file.file_hash)
        r = risk.get('risk_level', -1)
    else:
        r = int(risk)
    # kafka publish

    return Response(file=BaseResponse(hash=event.file.file_hash, risk_level=r),
                    process=BaseResponse(hash=event.last_access.hash, risk_level=r))


Instrumentator().instrument(app).expose(app)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
