from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import Header, Depends, HTTPException
from starlette import status

from app.core.db import get_database
from app.users.schemas import COLLECTION_NAME
from app.config import MONGO_INITDB_DATABASE


async def get_or_create_user(authorization=Header(None), db: AsyncIOMotorClient = Depends(get_database)) -> dict:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please send id of user")
    user = await db[MONGO_INITDB_DATABASE][COLLECTION_NAME].find_one({'telegram_id': authorization})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exists")
    return dict(user)
