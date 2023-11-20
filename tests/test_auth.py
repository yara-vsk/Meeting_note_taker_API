from httpx import AsyncClient

from tests.conftest import client


def test_register():
    response = client.post('auth/register', json={

        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": 0,
    })

    assert response.status_code == 201
    assert response.json() == {
        "email": "user@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": 1,
    }


async def test_login(ac: AsyncClient):
    response = await ac.post('auth/jwt/login', data={
        "username": "user@example.com",
        "password": "string",
    })
    assert response.status_code == 200


async def test_get_me(ac: AsyncClient, get_access_token):
    response = await ac.get('users/me', headers={"Authorization": "Bearer " + get_access_token})
    assert response.status_code == 200
    assert response.json() == {
        "email": "user@example.com",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": 1,
    }


