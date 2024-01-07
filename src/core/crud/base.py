from typing import Iterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import models


async def get_items(
    db: AsyncSession, model, skip: int | None = None, limit: int | None = None
) -> Iterator[models.Base]:
    return await db.scalars(select(model).offset(skip).limit(limit))


async def get_item(
    db: AsyncSession, model, id: str
) -> Iterator[models.Base]:
    return await db.get(model, id)
