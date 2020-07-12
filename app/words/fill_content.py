import json
import asyncio

from app.core.db import get_database, connect_to_mongo, close_mongo_connection
from app.words.schemas import COLLECTION_NAME
from app.config import MONGO_INITDB_DATABASE


async def fill_content(path: str):
    try:
        await connect_to_mongo()
        db = await get_database()
        with open(path) as f:
            data = json.load(f)
            await db[MONGO_INITDB_DATABASE][COLLECTION_NAME].insert_many(data)
    finally:
        await close_mongo_connection()

filepath = input('Please enter path to file with content: ')

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(fill_content(filepath))
