import pytest
from httpx import AsyncClient
from main import app


@pytest.fixture
def non_mocked_hosts() -> list:
    return ["test.host"]


@pytest.mark.asyncio
async def test_user_is_created():

    user_data = {
        "full_name": "Zac Oyama",
        "email": "zoyama@gmail.com",
        "username": "zac.oyama",
        "password": "asdawr2sd"
    }

    async with AsyncClient(app=app, base_url="http://test.host") as ac:
        response = await ac.post("/users", json=user_data)

    assert response.status_code == 201
    assert response.json() == {
        "id": 0,
        "full_name": "Zac Oyama",
        "email": "zoyama@gmail.com",
        "username": "zac.oyama",
        "password": "asdawr2sd"
    }


@pytest.mark.asyncio
async def test_user_fails_to_create():
    user_data = {
        "full_name": "Zac Oyama",
        "email": "zoyama@gmail.com",
        "username": "zac.oyama",
    }

    async with AsyncClient(app=app, base_url="http://test.host") as ac:
        response = await ac.post("/users", json=user_data)

    data = response.json()

    assert response.status_code == 422
    assert data['detail'][0]['msg'] == 'Field required'
    assert data['detail'][0]['loc'] == ['body', 'password']
