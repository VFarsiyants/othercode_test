from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.user import User


class Post(Base):
    __tablename__ = "post"
    owner_collumn = "author_id"

    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    text: Mapped[str] = mapped_column(Text())
    author_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(), server_default=now())

    author: Mapped['User'] = relationship(back_populates="posts")
