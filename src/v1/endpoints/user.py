from typing import List

from fastapi import APIRouter, Depends

from src.core import models, schemas

from .dependencies import GetObject, GetObjects, get_current_auth_user

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
def get_jwt_token(user: schemas.User = Depends(get_current_auth_user)):
    return user
