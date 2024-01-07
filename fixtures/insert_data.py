import json

from sqlalchemy.dialects.postgresql import insert

from src.core import models


async def insert_or_update(session, fixture_file, model, constraint):
    with open(fixture_file, 'r', encoding='utf-8') as f:
        fixture_data = json.load(f)
    for data in fixture_data:
        insert_stmt = insert(model).values(**data)
        do_update_stmt = insert_stmt.on_conflict_do_update(
            constraint=constraint,
            set_=data
        )
        await session.execute(do_update_stmt)


async def insert_data(session):
    await insert_or_update(
        session, 'fixtures/role.json', models.Role, 'role_pkey')
    await insert_or_update(
        session, 'fixtures/permissions.json', models.Permission,
        'permission_pkey')
    await insert_or_update(
        session, 'fixtures/permission_to_role.json',
        models.permission_to_role,
        'permission_to_role_role_id_permission_id_key')
    await session.commit()
