import asyncio

from fixtures.insert_data import insert_data
from src.core.models.database import async_session


async def insert_fixtures():
    async with async_session() as session:
        await insert_data(session)

asyncio.run(insert_fixtures())
