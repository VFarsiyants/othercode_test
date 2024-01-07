from fastapi import Depends, HTTPException, Query, Request, Response, status
from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import check_password, decode_jwt
from src.core import crud, schemas
from src.core.models.exeptions import IncorrectFilterExeption
from src.dependencies import get_db


async def validate_auth_data(
    auth_data: schemas.UserAuthInfo,
    db: AsyncSession = Depends(get_db)
):
    unauth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid email or password'
    )

    if not (user := await crud.get_user_by_email(db, auth_data.email)):
        raise unauth_exception

    if check_password(
        password=auth_data.password,
        hash=user.hashed_password
    ):
        return user

    raise unauth_exception


http_bearer = HTTPBearer(auto_error=False)


async def get_current_auth_user(
    credentials: str = Depends(http_bearer),
    db: AsyncSession = Depends(get_db)
) -> schemas.User:
    if credentials is None:
        return None
    token = credentials.credentials
    payload = {}
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}"
        )
    email = payload.get('sub', None)
    if email:
        return await crud.get_user_by_email(db, email)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )


REQUEST_TO_ACTION = {
    'POST': 'CREATE',
    'PUT': 'UPDATE',
    'GET': 'READ',
    'DELETE': 'DELETE',
}


class CheckPerm:
    def __init__(self, resource, action):
        self.action = action
        self.resource = resource

    async def __call__(
        self,
        db: AsyncSession = Depends(get_db),
        user: schemas.User = Depends(get_current_auth_user),
    ):
        has_permission = await crud.check_permission(
            db, self.resource, self.action, user=user)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='You don\'t have enough rights to perform this operation')


class GetObject:
    def __init__(self, model, resource):
        self.model = model
        self.resource = resource

    async def __call__(
        self,
        request: Request,
        id: str,
        user=Depends(get_current_auth_user),
        db: AsyncSession = Depends(get_db),
    ):
        item = await crud.get_item(db, self.model, id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        action = REQUEST_TO_ACTION[request.method]
        # Grant permission if owner does something with instance
        if self.model.owner_collumn and user\
                and getattr(item, self.model.owner_collumn) == user.id:
            has_permission = True
        else:
            has_permission = await crud.check_permission(
                db, self.resource, action, user=user)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='You don\'t have enough rights to perform this operation')
        return item


class GetObjects:
    def __init__(self, model, resource):
        self.model = model
        self.resource = resource

    async def __call__(
        self,
        request: Request,
        response: Response,
        skip: int | None = None,
        limit: int | None = None,
        user=Depends(get_current_auth_user),
        db: AsyncSession = Depends(get_db),
        base_filter: str | None = Query(
            default=None,
            examples=[
                '{ "author__firstname": "Example", "name": "Example post name" }'
            ])
    ):
        try:
            items = await crud.get_items(
                db, self.model, skip=skip, limit=limit, filter=base_filter)
        except IncorrectFilterExeption:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect base filter parameter'
            )
        action = REQUEST_TO_ACTION[request.method]
        has_permission = await crud.check_permission(
            db, self.resource, action, user=user)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='You don\'t have enough rights to perform this operation')
        response.headers['X-Total-Count'] = str(await crud.get_total_count(
            db, self.model, filter=base_filter))
        return items
