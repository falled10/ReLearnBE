from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
import random

from app.words.schemas import COLLECTION_NAME as WORDS_COLLECTION
from app.users.schemas import COLLECTION_NAME as USERS_COLLECTION
from app.config import MONGO_INITDB_DATABASE


async def get_random_word(db: AsyncIOMotorClient) -> dict:
    result = {}
    words = db[MONGO_INITDB_DATABASE][WORDS_COLLECTION].aggregate([{'$sample': {'size': 4}}])
    words = await words.to_list(length=4)
    if words:
        words[0].update({'id': str(words[0]['_id'])})
        result['word'] = words[0]
        variants = [w['word'] for w in words]
        random.shuffle(variants)
        result['variants'] = variants
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no word on database')
    return result


async def set_answer(word_id: str, user_id: str, db: AsyncIOMotorClient):
    await db[MONGO_INITDB_DATABASE][USERS_COLLECTION].update_one({'telegram_id': user_id},
                                                                {'$push': {'words': word_id}})
