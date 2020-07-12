from typing import Optional

from app.core.schemas import DBModelSchema, CamelCaseSchema


COLLECTION_NAME = "users_collection"


class TelegramUserSchema(CamelCaseSchema):
    """DB model for telegram user
    """
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    words: list = []

    @staticmethod
    def get_collection_name():
        return COLLECTION_NAME


class CreateTelegramUserSchema(DBModelSchema):
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    words: list = []
