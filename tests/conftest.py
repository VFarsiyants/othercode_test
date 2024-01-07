import pytest
from fixtures.insert_data import insert_data
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.auth.utils import encode_jwt
from src.core import crud, schemas
from src.core.models import Base
from src.core.settings import db_settings
from src.dependencies import get_db
from src.main import app

TEST_DB_NAME = 'test_' + db_settings.DB_NAME
TEST_DB_ECHO = False

test_db_url = f"postgresql+asyncpg://{db_settings.DB_USER}:{db_settings.DB_PASSWORD}@{db_settings.DB_HOST}:{db_settings.DB_PORT}/{TEST_DB_NAME}"

engine_test = create_async_engine(
    test_db_url, echo=False, poolclass=NullPool)
test_async_session = async_sessionmaker(engine_test, expire_on_commit=False)


async def ovverride_get_db():
    async with test_async_session() as session:
        yield session

app.dependency_overrides[get_db] = ovverride_get_db


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with test_async_session() as session:
        await insert_data(session)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_new_user_token(session, user_data: schemas.UserCreate):
    await crud.create_user(session, user_data)
    jwt_payload = {
        "sub": user_data.email,
        "name": f"{user_data.firstname} {user_data.lastname}"
    }
    return encode_jwt(jwt_payload)


@pytest.fixture(autouse=True, scope='session')
async def admin_token(prepare_database):
    async with test_async_session() as session:
        user_data = schemas.UserCreate(
            firstname="admin",
            lastname="admin",
            email="admin@example.com",
            password="admin"
        )
        token = await get_new_user_token(session, user_data)
        yield token


@pytest.fixture(scope='session')
async def ac():
    async with AsyncClient(app=app, base_url='http://test/api/v1') as ac:
        yield ac
