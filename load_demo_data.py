import asyncio
import random

from faker import Faker

from src.core import crud, schemas
from src.core.models.database import async_session

fake = Faker()

users_preset = [
    {
        'firstname': 'Admin',
        'lastname': 'Admin',
        'email': 'aadmin@example.com',
    },
    {
        'firstname': 'User',
        'lastname': 'User',
        'email': 'uuser@example.com',
    },
    {
        'firstname': 'Moderator',
        'lastname': 'Moderator',
        'email': 'mmoderator@example.com',
    }
]

random_users = []


def get_random_post():
    title = fake.sentence(nb_words=random.randint(1, 5)).replace('.', '')
    content = ''

    for _ in range(random.randint(5, 10)):
        content += fake.sentence(nb_words=random.randint(5, 20)) + ' '
    return schemas.PostCreate(name=title, text=content)


for _ in range(10):
    firstname, lastname = fake.unique.first_name(), fake.unique.last_name()
    password = f'{firstname[0]}{lastname}'
    email = f'{password}@example.com'
    random_users.append({
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'password': password,
    })

created_users = []


async def create_ord_users():
    async with async_session() as session:
        admin = users_preset[0]
        admin = await crud.create_user(session, schemas.UserCreate(
            **admin, password=f'{admin["firstname"][0]}{admin["lastname"]}'
        ))
        await crud.set_user_role(session, admin.email, 'admin')
        user = users_preset[1]
        user = await crud.create_user(session, schemas.UserCreate(
            **user, password=f'{user["firstname"][0]}{user["lastname"]}'
        ))
        await crud.set_user_role(session, user.email, 'user')
        moderator = users_preset[2]
        moderator = await crud.create_user(session, schemas.UserCreate(
            **moderator, password=f'{moderator["firstname"][0]}{moderator["lastname"]}'
        ))
        await crud.set_user_role(session, moderator.email, 'moderator')
        created_users.append(admin)
        created_users.append(user)
        created_users.append(moderator)
        await session.commit()


async def create_random_users():
    async with async_session() as session:
        for user in random_users:
            db_user = await crud.create_user(session, schemas.UserCreate(**user))
            created_users.append(db_user)


async def create_random_posts():
    async with async_session() as session:
        for user in created_users:
            post_numbers = random.randint(5, 10)
            for _ in range(post_numbers):
                await crud.create_post(session, user, get_random_post())
        await session.commit()


async def main():
    await create_ord_users()
    await create_random_users()
    await create_random_posts()


asyncio.run(main())
