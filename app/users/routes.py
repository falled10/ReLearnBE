from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.users.schemas import CreateTelegramUserSchema, TelegramUserSchema
from app.users.crud import create_user, get_user_by_telegram_id
from app.users.dependencies import get_or_create_user
from app.core.db import get_database


router = APIRouter()


@router.post('', response_model=TelegramUserSchema)
async def create_new_user(user: CreateTelegramUserSchema, db: AsyncIOMotorClient = Depends(get_database)):
    user = await create_user(db, user)
    return user


@router.get('/me', response_model=TelegramUserSchema)
async def get_current_user(db: AsyncIOMotorClient = Depends(get_database),
                           user: dict = Depends(get_or_create_user)):
    user = await get_user_by_telegram_id(user['telegram_id'], db)
    return user
