from httpx import AsyncClient


async def test_register(ac: AsyncClient):
    response = await ac.post('/register/', json={
        "firstname": "Firstname",
        "lastname": "Lastname",
        "email": "flastname@example.com",
        "password": "password"
    })

    assert response.status_code == 201, 'User was not created'


async def test_get_token(ac: AsyncClient):
    response = await ac.post('/token/', json={
        "email": "flastname@example.com",
        "password": "password"
    })

    assert response.status_code == 200, 'Incorrect status on login operation'
    assert response.json().get('access_token', None), 'Token has not bee provided'
