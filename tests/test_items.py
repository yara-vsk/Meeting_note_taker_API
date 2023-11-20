import os
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.models.items import Item
from tests.conftest import async_session_maker

file_path = os.path.join(os.path.dirname(__file__), 'media_for_tests', 'audio_test.m4a')


async def test_add_item(ac: AsyncClient, get_access_token, get_meeting_id):
    with open(file_path, 'rb') as file:
        response = await ac.post(f'meetings/{get_meeting_id}/items',
                                 headers={
                                     "Authorization": "Bearer " + get_access_token},
                                 data={
                                     "description": "Test description.",
                                 },
                                 files={'file': file}
                                 )
    async with async_session_maker() as session:
        stmt = select(Item).where(Item.id == 1).options(selectinload('*'))
        item = await session.scalar(stmt)
    assert response.status_code == 200
    assert response.json()['description'] == "Test description."
    assert os.path.isfile(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', str(item.audio_record.file_name))) is True


async def test_get_items(ac: AsyncClient, get_access_token, get_meeting_id):
    response = await ac.get(f'meetings/{get_meeting_id}/items',
                            headers={
                                "Authorization": "Bearer " + get_access_token}
                            )
    async with async_session_maker() as session:
        stmt = select(Item).options(selectinload('*'))
        result = await session.execute(stmt)
        items = result.scalars().all()

    assert response.status_code == 200
    assert len(response.json()) == len(items)


async def test_delete_items(ac: AsyncClient, get_access_token, get_meeting_id):
    response = await ac.delete(f'meetings/{get_meeting_id}/items/1',
                               headers={
                                   "Authorization": "Bearer " + get_access_token}
                               )
    async with async_session_maker() as session:
        stmt = select(Item).options(selectinload('*'))
        result = await session.execute(stmt)
        items = result.scalars().all()

    assert response.status_code == 200
    assert len(items) == 0
    assert response.json()['Status'] == "Item id=1 was deleted"
