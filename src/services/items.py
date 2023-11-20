import os
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
import aiofiles as aiofiles
from src.config import BASE_DIR
from src.schemas.items import ItemsSchemaAdd, ItemsSchemaOut
from src.utils.background_tasks import audio_note_extractor
from src.utils.unitofwork import IUnitOfWork


DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte


class ItemsService:

    async def add_item(self, uow: IUnitOfWork, description: str, audio_file, back_task):
        audio_file_name = f'{uuid4()}.' + str(audio_file.filename.split('.')[1])

        async with uow:
            meeting = await self.check_meeting_access(uow)
            item = await uow.item.add_one({
                'description': description,
                'meeting_id': meeting.id
            })
            audio_record = await uow.audio_record.add_one({
                'file_name': str(audio_file_name),
                'item_id': item.id
            })
            await uow.commit()
            await self.write_audio_file(os.path.join(BASE_DIR, 'media', audio_file_name), audio_file,
                                        audio_record.id)
            audio_note_extractor.delay(os.path.join(BASE_DIR, 'media', audio_file_name), audio_record.id)
            item.audio_record = audio_record
            item_pd = ItemsSchemaOut(**item.__dict__)
            return item_pd

    async def get_item(self, uow: IUnitOfWork, item_id: int):
        async with uow:
            meeting = await self.check_meeting_access(uow)
            try:
                item = await uow.item.find_one({'id': item_id, 'meeting_id': meeting.id})
            except NoResultFound:
                raise HTTPException(status_code=404, detail="Not found")
            item_pd = ItemsSchemaOut(**item.__dict__)
            return item_pd

    async def edit_item(self, uow: IUnitOfWork, item_id: int, item_pd: ItemsSchemaAdd):
        item_dict = item_pd.model_dump()
        async with uow:
            meeting = await self.check_meeting_access(uow)
            try:
                item = await uow.item.edit_one({'id': item_id, 'meeting_id': meeting.id},  item_dict)
                await uow.commit()
            except NoResultFound:
                raise HTTPException(status_code=404, detail="Not found")
            item_pd = ItemsSchemaOut(**item.__dict__)
            return item_pd

    async def delete_item(self, uow: IUnitOfWork, item_id: int):
        async with uow:
            try:
                meeting = await self.check_meeting_access(uow)
                audio_record = await uow.audio_record.find_one({'item_id': item_id})
                await uow.item.delete_one({'id': item_id, 'meeting_id': meeting.id})
                self.delete_audio_file(audio_record.file_name)
                await uow.commit()
            except NoResultFound:
                raise HTTPException(status_code=404, detail="Not found")
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail="Not found")
            return

    async def get_items(self, uow: IUnitOfWork):
        async with uow:
            meeting = await self.check_meeting_access(uow)
            items = await uow.item.find_all({'meeting_id': meeting.id})
            items_pd_list = [ItemsSchemaOut(**item.__dict__) for item in items]
            return items_pd_list

    async def write_audio_file(self, file_path, audio_file, audio_record_id):
        async with aiofiles.open(file_path, 'wb') as buffer:
            while chunk := await audio_file.read(DEFAULT_CHUNK_SIZE):
                await buffer.write(chunk)

    @staticmethod
    def delete_audio_file(audio_file_name):
        os.remove(os.path.join(BASE_DIR, 'media', audio_file_name))

    @staticmethod
    async def check_meeting_access(uow_after_with):
        try:
            meeting = await uow_after_with.meeting.find_one({'id': int(uow_after_with.current_meeting_id)})
            if meeting.user_id != uow_after_with.current_user.id:
                raise NoResultFound
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Not found")
        except ValueError:
            raise HTTPException(status_code=400, detail="'meetingID' must be an integer")
        return meeting
