from typing import List

from app.core.schemas import CamelCaseSchema


COLLECTION_NAME = 'words_collection'


class WordSchema(CamelCaseSchema):
    id: str
    word: str
    transcription: str
    translation: str


class RandomWordSchema(CamelCaseSchema):
    """Use this schema if you need to get random word with variants
    """
    word: WordSchema
    variants: List[str]


class AnswerSchema(CamelCaseSchema):
    word_id: str
