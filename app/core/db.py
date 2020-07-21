from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGO_URL


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo() -> None:
    db.client = AsyncIOMotorClient(MONGO_URL, maxPoolSize=10, minPoolSize=10)


async def close_mongo_connection() -> None:
    db.client.close()
