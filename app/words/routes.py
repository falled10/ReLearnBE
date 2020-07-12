from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import APIRouter, Depends

from app.core.db import get_database
from app.words.crud import get_random_word, set_answer, get_translation_by_word
from app.words.schemas import RandomWordSchema, AnswerSchema, WordSchema
from app.users.dependencies import get_or_create_user

router = APIRouter()


@router.get('/random_word', response_model=RandomWordSchema)
async def random_word(db: AsyncIOMotorClient = Depends(get_database),
                      user: dict = Depends(get_or_create_user)):
    word = await get_random_word(user['words'], db)
    return word


@router.post('/answer', status_code=204)
async def add_new_answer(answer: AnswerSchema, db: AsyncIOMotorClient = Depends(get_database),
                         user: dict = Depends(get_or_create_user)):
    answer = answer.dict()
    await set_answer(answer['word_id'], user['telegram_id'], db)
    return


@router.get('/{word}', response_model=WordSchema)
async def get_word_translation(word: str, db: AsyncIOMotorClient = Depends(get_database)):
    word = await get_translation_by_word(word, db)
    return word
