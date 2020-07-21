from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status

from app.core.config import MONGO_INITDB_DATABASE
from app.users.schemas import COLLECTION_NAME


async def validate_unique_telegram_id(value: str, db: AsyncIOMotorClient) -> str:
    """Use this validator before create new user
    """
    db_user = await db[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one(
        {'telegram_id': value})
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with that telegram id already exist')
    return value
