from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.users.schemas import CreateTelegramUserSchema, TelegramUserSchema
from app.users.crud import create_user, get_user_by_telegram_id
from app.core.db import get_database


router = APIRouter()


@router.post('', response_model=TelegramUserSchema)
async def create_new_user(user: CreateTelegramUserSchema, db: AsyncIOMotorClient = Depends(get_database)):
    user = await create_user(db, user)
    return user


@router.get('/{telegram_id}', response_model=TelegramUserSchema)
async def get_one_user(telegram_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    user = await get_user_by_telegram_id(telegram_id, db)
    return user
