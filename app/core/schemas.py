from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.utils import to_camel


class CamelCaseSchema(BaseModel):

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class DBModelSchema(CamelCaseSchema):
    created_at: Optional[datetime] = datetime.now()

    @staticmethod
    def get_collection_name():
        return 'base_collection'
