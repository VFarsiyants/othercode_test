from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import encode_jwt
from src.core import crud, schemas
from src.dependencies import get_db

from .dependencies import validate_auth_data

router = APIRouter()


@router.post("/register/", response_model=schemas.User, status_code=201)
async def register_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_user(db=db, user=user)


@router.post("/token/", response_model=schemas.TokenInfo)
def get_jwt_token(user: schemas.User = Depends(validate_auth_data)):
    jwt_payload = {
        "sub": user.email,
        "name": f"{user.firstname} {user.lastname}"
    }
    token = encode_jwt(jwt_payload)
    return schemas.TokenInfo(
        access_token=token,
        token_type="Bearer"
    )
