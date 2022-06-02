import hashlib
import random

import pytest
from starlette.testclient import TestClient

from events_api.main import app as events_app
from files_api.testdb import TestDatabase
from files_api.main import app as files_app


@pytest.fixture
def events_client():
    return TestClient(events_app)


@pytest.fixture()
def files_client():
    return TestClient(files_app)


@pytest.fixture()
async def mongo_client():
    db = TestDatabase()
    await db.drop_collection()
    yield
    await db.drop_collection()


def generate_random_file():
    file_contents = [0x40, 0x5A]
    file_contents.extend(random.randbytes(random.randint(10240, 1024000)))
    file_bytes = bytes(file_contents)
    return file_bytes


@pytest.fixture
async def mongo_client():
    # db trebuie sa ruleze in docker
    db = TestDatabase()
    await db.drop_collection()
    yield db
    await db.drop_collection()


@pytest.mark.asyncio
async def test_events(events_client, files_client, mongo_client):
    random_file = b"MZ\xd8\xee?\xa1r\xec\x8c\x9c\xcb\x16\x16q\x9d \xf2g\xc4N\xf0i\xd3(\xe8YF\xbbE\x12D\x94\x1c\xff\xb0w\xddH?*\x86\x02Fn\x19\xc3W_y\xcf\xb6\xf8)\x80c~%\xbb\rC\xb9 \xb7s\x81\xc7\x83\xf8\x81F\xcd8\xfe\xd2\x9c\xef\xfa\n\xb6\x0b\x08\x8e\x86IX:\x9bo\xd3\x0b\xc6\x05\x89\xb3\x94PD\xff\x10)"
    random_file_hash = hashlib.md5(random_file).hexdigest()
    event = {
        "device": {"id": "7605e08f-edbb-4a14-b031-6c8c1cb46300", "os": "windows"},
        "file": {
            "file_hash": random_file_hash,
            "file_path": "/sys/441421f8-9f32-490b-9598-c28c743d47a5/ntfs",
            "time": {"a": 1626992365005, "m": 1590366615103},
        },
        "last_access": {
            "hash": "250f5c44fe5b6a45600ecd7151178f5d",
            "path": "/dev/b2e8e4f4-7efb-42b8-b233-2a4547dc4af4/cat",
            "pid": 3074,
        },
    }

    # Test with non-existing file
    response = events_client.post("/events", json=event)
    assert response.status_code == 200
    assert response.json() == {
        "file": {"hash": random_file_hash, "risk_level": -1},
        "process": {"hash": "250f5c44fe5b6a45600ecd7151178f5d", "risk_level": -1},
    }

    # Scan file
    response = files_client.post("scan-file", files={"file": random_file})
    assert response.status_code == 200

    # Test again /w uploaded file
    response = events_client.post("/events", json=event)
    assert response.status_code == 200
    assert response.json() == {
        "file": {"hash": random_file_hash, "risk_level": 0},
        "process": {"hash": "250f5c44fe5b6a45600ecd7151178f5d", "risk_level": 0},
    }


@pytest.mark.parametrize("numar1,numar2,rezultat", [
    (1, 1, 2),
    (1, 5, 6),
    (4, 5, 9),
])
def test_param(numar1, numar2, rezultat):
    assert numar1 + numar2 == rezultat

