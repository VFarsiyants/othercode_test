from typing import Iterator

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import models
from src.core.models.filtering import get_joins_filters


def _add_joins_filters(stmt, filter, model):
    joins, filters = get_joins_filters(model, filter)
    for join in joins:
        stmt = stmt.join(join)
    for filter in filters:
        stmt = stmt.where(filter)
    return stmt


async def get_items(
    db: AsyncSession, model, skip: int | None = None, limit: int | None = None,
    filter: str = None
) -> Iterator[models.Base]:
    stmt = select(model).offset(skip).limit(limit)
    if filter:
        stmt = _add_joins_filters(stmt, filter, model)
    return await db.scalars(stmt)


async def get_total_count(
    db: AsyncSession, model, filter: str = None
) -> Iterator[models.Base]:
    stmt = select(func.count(model.id))
    if filter:
        stmt = _add_joins_filters(stmt, filter, model)
    count = await db.scalar(stmt)
    return count


async def get_item(
    db: AsyncSession, model, id: str
) -> Iterator[models.Base]:
    return await db.get(model, id)
