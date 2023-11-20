import asyncio

from httpx import AsyncClient
from sqlalchemy import NullPool, select
from starlette.testclient import TestClient

from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, MODE
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import pytest
from src.db import get_async_session
from src.main import app
from src.db import Base
from src.models.items import Item, AudioRecord
from src.models.users import User
from src.models.meetings import Meeting

if MODE != 'TEST':
    raise Exception

DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='function')
async def get_access_token(ac: AsyncClient):
    response = await ac.post('auth/jwt/login', data={
        "username": "user@example.com",
        "password": 'string',
    })
    return response.json()['access_token']


@pytest.fixture(scope='function')
async def get_access_token_with_no_perm(ac: AsyncClient):
    await ac.post('auth/register', json={

        "email": "user2@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "id": 0,
    })
    response = await ac.post('auth/jwt/login', data={
        "username": "user2@example.com",
        "password": 'string',
    })
    return response.json()['access_token']


@pytest.fixture(scope='function')
async def get_meeting_id(ac: AsyncClient, get_access_token):
    async with async_session_maker() as session:
        stmt = select(Meeting)
        result = await session.execute(stmt)
        meetings = result.scalars().all()
    if meetings:
        return meetings[0].id
    response = await ac.post('meetings',
                             headers={
                                 "Authorization": "Bearer " + get_access_token},
                             json={
                                 "name": "First meeting",
                             })

    return response.json()['id']