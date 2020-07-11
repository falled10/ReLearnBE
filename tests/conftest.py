import pytest

from fastapi.testclient import TestClient

from app.config import MONGO_INITDB_DATABASE
from app.core.db import get_database, connect_to_mongo, close_mongo_connection
from main import app


@pytest.yield_fixture(autouse=True)
async def collections():
    await connect_to_mongo()
    db = await get_database()
    yield
    await db.drop_database(MONGO_INITDB_DATABASE)
    await close_mongo_connection()


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client
