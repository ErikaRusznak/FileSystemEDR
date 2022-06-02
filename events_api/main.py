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

    r = -1
    if risk is None:
        risk = await db.find_data(some_key=event.file.file_hash)
    if risk is not None:
        r = risk['risk_level']
    else:
        r = -1;

    return Response(file=BaseResponse(hash=event.file.file_hash, risk_level=r),
                    process=BaseResponse(hash=event.last_access.hash, risk_level=r))


Instrumentator().instrument(app).expose(app)
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
