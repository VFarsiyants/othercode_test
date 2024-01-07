from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import exists

from src.auth.utils import hash_password
from src.core import models, schemas


async def get_role(db: AsyncSession, role_name):
    result = await db.scalars(select(models.Role).filter_by(
        name=role_name).limit(1))
    return result.first()


async def create_user(
    db: AsyncSession,
    user: schemas.UserCreate
) -> models.User:
    hashed_password = hash_password(user.password).decode()
    db_user = models.User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    await set_user_role(db, user.email, 'user')
    return db_user


async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> models.User:
    stmt = select(models.User).options(selectinload(
        models.User.roles)).where(models.User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


async def set_user_role(db: AsyncSession, user_email: str, role_name: str):
    stmt = select(models.User).options(selectinload(
        models.User.roles)).filter_by(email=user_email)
    result = await db.scalars(stmt)
    user = result.first()
    if user is None:
        raise ValueError('User with given email not found')

    role = await get_role(db, role_name)

    user.roles.append(role)
    await db.commit()


async def get_user_roles(db: AsyncSession, user_email: str):
    user = await get_user_by_email(db, user_email)
    return user.roles


async def check_permission(
        db: AsyncSession, resource, action, user: models.User = None):
    if user:
        roles = await get_user_roles(db, user.email)
    else:
        roles = [await get_role(db, 'anonimus')]

    roles = (str(role.id) for role in roles)

    stmt = select(models.Permission).join(
        models.Role, models.Permission.roles
    ).where(
        and_(
            models.Role.id.in_(roles),
            models.Permission.code == action,
            models.Permission.resource == resource
        )
    )

    stmt = exists(stmt).select()
    result = await db.execute(stmt)
    return result.first()[0]
