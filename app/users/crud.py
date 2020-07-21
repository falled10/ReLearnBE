from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status

from app.users.schemas import CreateTelegramUserSchema, COLLECTION_NAME
from app.users.validators import validate_unique_telegram_id
from app.core.config import MONGO_INITDB_DATABASE


async def create_user(conn: AsyncIOMotorClient, user: CreateTelegramUserSchema):
    await validate_unique_telegram_id(user.dict()['telegram_id'], conn)
    await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].insert_one(user.dict())
    return user


async def get_user_by_telegram_id(telegram_id: str, conn: AsyncIOMotorClient):
    user = await conn[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one({'telegram_id': telegram_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
