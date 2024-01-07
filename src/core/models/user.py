from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.post import Post
    from src.core.models.role import Role


user_to_role = Table(
    "user_to_role",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("role_id", ForeignKey("role.id")),
    UniqueConstraint("user_id", "role_id"),
)


class User(Base):
    __tablename__ = "user"
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(300), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(300), nullable=False)
    roles: Mapped[List['Role']] = relationship(secondary=user_to_role)

    posts: Mapped[List['Post']] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )
