from typing import Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    firstname: str
    lastname: Union[str, None] = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID


class UserAuthInfo(BaseModel):
    email: EmailStr
    password: str
