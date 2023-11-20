from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.meetings import Meeting
from tests.conftest import async_session_maker


async def test_create_meeting(ac: AsyncClient, get_access_token):
    response = await ac.post('meetings',
                             headers={
                                 "Authorization": "Bearer " + get_access_token},
                             json={
                                 "name": "First meeting",
                             })
    assert response.status_code == 200
    assert response.json()['name'] == "First meeting"
    assert response.json()['user']['email'] == 'user@example.com'


async def test_get_meetings(ac: AsyncClient, get_access_token):
    response = await ac.get('meetings',
                            headers={
                                "Authorization": "Bearer " + get_access_token})
    async with async_session_maker() as session:
        stmt = select(Meeting).options(selectinload(Meeting.user))
        result = await session.execute(stmt)
        meetings = result.scalars().all()
    assert response.status_code == 200
    assert len(response.json()) == len(meetings)


async def test_get_meetings_user_without_perm(ac: AsyncClient, get_access_token_with_no_perm):
    response = await ac.get('meetings',
                            headers={
                                "Authorization": "Bearer " + get_access_token_with_no_perm})
    assert response.status_code == 200
    assert len(response.json()) == 0



async def test_get_meeting(ac: AsyncClient, get_access_token):
    response = await ac.get('meetings/1',
                            headers={
                                "Authorization": "Bearer " + get_access_token})
    async with async_session_maker() as session:
        stmt = select(Meeting).where(Meeting.id == 1).options(selectinload(Meeting.user))
        result = await session.execute(stmt)
        meeting = result.scalar()
    assert response.status_code == 200
    assert response.json()['name'] == meeting.name
    assert response.json()['id'] == meeting.id


async def test_get_meeting_without_perm(ac: AsyncClient, get_access_token_with_no_perm):
    response = await ac.get('meetings/1',
                            headers={
                                "Authorization": "Bearer " + get_access_token_with_no_perm})
    async with async_session_maker() as session:
        stmt = select(Meeting).where(Meeting.id == 1).options(selectinload(Meeting.user))
        result = await session.execute(stmt)
        meeting = result.scalar()
    assert response.status_code == 404
    assert meeting.id == 1


async def test_put_meeting(ac: AsyncClient, get_access_token):
    response = await ac.put('meetings/1',
                            headers={
                                "Authorization": "Bearer " + get_access_token},
                            json={
                                "name": "First meeting version 2",
                            })
    async with async_session_maker() as session:
        stmt = select(Meeting).where(Meeting.id == 1).options(selectinload(Meeting.user))
        result = await session.execute(stmt)
        meeting = result.scalar()
    assert response.status_code == 200
    assert response.json()['name'] == 'First meeting version 2'
    assert response.json()['id'] == meeting.id


async def test_delete_meeting(ac: AsyncClient, get_access_token):
    response = await ac.delete('meetings/1',
                               headers={
                                   "Authorization": "Bearer " + get_access_token})
    async with async_session_maker() as session:
        stmt = select(Meeting).where(Meeting.id == 1).options(selectinload(Meeting.user))
        result = await session.execute(stmt)
        meetings = result.scalars().all()
    assert response.status_code == 200
    assert response.json()['Status'] == "Meeting id=1 was deleted"
    assert len(meetings) == 0

