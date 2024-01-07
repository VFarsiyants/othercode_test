from httpx import AsyncClient


async def test_create_post(ac: AsyncClient, admin_token):
    response = await ac.post(
        '/post/',
        headers={
            'authorization': f'Bearer {admin_token}'
        },
        json={
            "name": "string",
            "text": "string",
        })

    assert response.status_code == 201, 'Post was not created'


async def test_get_posts(ac: AsyncClient):
    response = await ac.get('/post/')

    assert response.status_code == 200, 'Unable to get posts'

    post_id = response.json()[0]['id']
    response = await ac.get(f'/post/{post_id}')

    assert response.status_code == 200, 'Unable to get details about posts'


async def test_delete_post(ac: AsyncClient, admin_token):
    response = await ac.get('/post/')
    post_id = response.json()[0]['id']
    response = await ac.delete(f'/post/{post_id}')
    assert response.status_code == 405, \
        'Delete should not be available for anonimus user'
    response = await ac.delete(
        f'/post/{post_id}',
        headers={
            'authorization': f'Bearer {admin_token}',
        }
    )
    assert response.status_code == 200, 'Unable to delete post'
