import argparse
import asyncio

from src.core.crud import set_user_role
from src.core.models.database import async_session

parser = argparse.ArgumentParser(
    prog='AssignUserToRole',
    description='Assign user with given email to desired role',
)
parser.add_argument('-e', '--email')
parser.add_argument('-r', '--role')

args = parser.parse_args()

user_email = args.email
role_name = args.role

if user_email is None:
    raise AttributeError('Pleas pass user email')

if role_name is None:
    raise AttributeError('Pleas pass role name')


async def main():
    async with async_session() as session:
        await set_user_role(session, user_email, role_name)


asyncio.run(main())
