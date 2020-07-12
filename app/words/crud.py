from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
import random

from app.words.schemas import COLLECTION_NAME as WORDS_COLLECTION
from app.users.schemas import COLLECTION_NAME as USERS_COLLECTION
from app.config import MONGO_INITDB_DATABASE


async def get_translation_by_word(word: str, db: AsyncIOMotorClient) -> dict:
    try:
        word = await db[MONGO_INITDB_DATABASE][WORDS_COLLECTION].find_one({'word': word})
    except InvalidId:
        raise HTTPException(status_code=404, detail="Word is not found")

    if not word:
        raise HTTPException(status_code=404, detail="Word is not found")
    word.update({'id': str(word['_id'])})
    return dict(word)


async def get_random_word(user_words, db: AsyncIOMotorClient) -> dict:
    """Returns random word with variants from words_collection
    and that is not in user words field
    """
    result = {}
    user_words = [ObjectId(i) for i in user_words]
    words = db[MONGO_INITDB_DATABASE][WORDS_COLLECTION].aggregate([{'$match': {'_id': {'$nin': user_words}}},
                                                                   {'$sample': {'size': 4}}])
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
    """Set word to user words depends on user answer
    """
    await db[MONGO_INITDB_DATABASE][USERS_COLLECTION].update_one({'telegram_id': user_id},
                                                                 {'$push': {'words': word_id}})
