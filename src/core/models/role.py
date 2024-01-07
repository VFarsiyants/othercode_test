from enum import Enum
from typing import List

from sqlalchemy import Column
from sqlalchemy import Enum as DbEnum
from sqlalchemy import ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base


class PermissionCodeEnum(Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


permission_to_role = Table(
    'permission_to_role',
    Base.metadata,
    Column("role_id", ForeignKey("role.id")),
    Column("permission_id", ForeignKey("permission.id")),
    UniqueConstraint("role_id", "permission_id"),
)


class Role(Base):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    permissions: Mapped[List['Permission']] = relationship(
        secondary=permission_to_role)


class Permission(Base):
    __tablename__ = 'permission'

    code: Mapped[str] = mapped_column(
        DbEnum(PermissionCodeEnum, name='permission_code'), nullable=False)
    resource: Mapped[str] = mapped_column(String(50), nullable=False)

    roles: Mapped[List['Role']] = relationship(
        secondary=permission_to_role, viewonly=True)
