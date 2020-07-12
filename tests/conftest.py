import pytest

from fastapi.testclient import TestClient

from app.config import MONGO_INITDB_DATABASE
from app.core.db import get_database, connect_to_mongo, close_mongo_connection
from app.words.schemas import COLLECTION_NAME as WORDS_COLLECTION
from app.users.schemas import CreateTelegramUserSchema, COLLECTION_NAME as USERS_COLLECTION
from main import app


@pytest.yield_fixture(autouse=True)
async def collections():
    """Fixture for clearing database after each test
    """
    try:
        await connect_to_mongo()
        db = await get_database()
        yield
        await db.drop_database(MONGO_INITDB_DATABASE)
    finally:
        await close_mongo_connection()


@pytest.fixture()
async def random_word():
    """Fixture for creating words inside words_collection
    """
    try:
        await connect_to_mongo()
        db = await get_database()
        data = [{'word': f'something{i}',
                 'transcription': '[something]',
                 'translation': 'щось'} for i in range(5)]
        word = await db[MONGO_INITDB_DATABASE][WORDS_COLLECTION].insert_many(data)
        yield word
    finally:
        await close_mongo_connection()


@pytest.fixture()
async def user():
    """Fixture for creating user inside user_collection
    """
    try:
        await connect_to_mongo()
        data = CreateTelegramUserSchema(**{'telegram_id': 'something',
                                           'username': 'something-else'}).dict()
        db = await get_database()
        await db[MONGO_INITDB_DATABASE][USERS_COLLECTION].insert_one(data)
        yield data
    finally:
        await close_mongo_connection()


@pytest.fixture()
def client():
    with TestClient(app) as client:
        yield client
