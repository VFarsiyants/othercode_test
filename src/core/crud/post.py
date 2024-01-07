from sqlalchemy.ext.asyncio import AsyncSession

from src.core import models, schemas


async def create_post(
    db: AsyncSession,
    user: schemas.User,
    post: schemas.PostCreate,
) -> models.User:
    db_post = models.Post(
        name=post.name,
        text=post.text,
        author_id=user.id
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def update_post(
    db: AsyncSession, post_instance: models.Post, post: schemas.PostBase,
):
    for field in post.model_fields:
        setattr(post_instance, field, getattr(post, field))
    await db.commit()
    await db.refresh(post_instance)
    return post_instance


async def delete_post(
    db: AsyncSession, post_instance: models.Post
):
    await db.delete(post_instance)
    await db.commit()
