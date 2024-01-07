from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    owner_collumn = None

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
