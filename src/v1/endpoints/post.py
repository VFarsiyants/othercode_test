from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import crud, models, schemas
from src.dependencies import get_db

from .dependencies import GetObject, GetObjects, get_current_auth_user

router = APIRouter(
    prefix='/post'
)


@router.post('/', response_model=schemas.Post, status_code=201)
async def create_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    user: schemas.User = Depends(get_current_auth_user)
):
    return await crud.create_post(db, user, post)


@router.get('/', response_model=List[schemas.Post])
def get_posts(
    items: List[models.Post] = Depends(GetObjects(models.Post, 'post'))
):
    return items


@router.get('/{id}', response_model=schemas.Post)
def get_post(
    item: models.Post = Depends(GetObject(models.Post, 'post'))
):
    return item


@router.delete('/{id}', status_code=200)
async def delete_post(
    item: models.Post = Depends(GetObject(models.Post, 'post')),
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_post(db, item)
    return


@router.put('/{id}', status_code=200, response_model=schemas.Post)
async def update_post(
    post: schemas.PostBase,
    item: models.Post = Depends(GetObject(models.Post, 'post')),
    db: AsyncSession = Depends(get_db),
):
    return await crud.update_post(db, item, post)
