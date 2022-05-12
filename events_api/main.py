from event_model import Event
from files_api.test import TestDatabase
from response_model import Response, BaseResponse
import uvicorn
from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
async def root():
    return {'title': 'Json System'}


@app.post("/events", response_model=Response)
async def add_event(event: Event) -> Response:

    db = TestDatabase()
    risk = await db.find_data(some_key=event.file.file_hash)
    r = -1
    if risk is not None:
        r = risk['risk_level']

    return Response(file=BaseResponse(hash=event.file.file_hash, risk_level=r),
                    process=BaseResponse(hash=event.last_access.hash, risk_level=r))


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)