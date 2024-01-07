from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import crud, models, schemas

from .dependencies import GetObject, GetObjects, get_current_auth_user, get_db

router = APIRouter(
    prefix='/user'
)


@router.get("/", response_model=List[schemas.User])
def get_users(
    users: List[models.User] = Depends(
        GetObjects(models.User, 'user'))
):
    return users


@router.get("/{id}", response_model=schemas.User)
def get_user(
        user: models.User = Depends(
            GetObject(models.User, 'user'))):
    return user


@router.get("/me/", response_model=schemas.User)
def get_current_user(user: schemas.User = Depends(get_current_auth_user)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You need to authorize first'
        )
    return user


@router.put("/{id}/add_to_role", response_model=schemas.User, status_code=200)
async def set_user_role(
    role: str,
    db: AsyncSession = Depends(get_db),
    user: models.User = Depends(
        GetObject(models.User, 'user'))
):
    await crud.set_user_role(db, user.email, role)
    return user
