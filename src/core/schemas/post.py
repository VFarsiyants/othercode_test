from datetime import datetime
from typing import Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    name: str
    text: Union[str, None] = None

    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: UUID
    author_id: UUID
    created_at: datetime
