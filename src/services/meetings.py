import os

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound

from src.config import BASE_DIR
from src.schemas.meetings import MeetingsSchema, MeetingsSchemaAdd
from src.utils.unitofwork import IUnitOfWork


class MeetingsService:

    async def add_meeting(self, uow: IUnitOfWork, meeting_data: MeetingsSchemaAdd):
        async with uow:
            meeting = await uow.meeting.add_one({
                'name': meeting_data.name,
                'user_id': uow.current_user.id
            })
            await uow.commit()
            meeting_pd = MeetingsSchema.model_validate(meeting)
            return meeting_pd

    async def get_meeting(self, uow: IUnitOfWork, meeting_id: int):
        async with uow:
            try:
                meeting = await uow.meeting.find_one({'id': meeting_id, 'user_id': uow.current_user.id})
            except NoResultFound:
                raise HTTPException(status_code=404, detail="Not found")
            meeting_pd = MeetingsSchema.model_validate(meeting)
            return meeting_pd

    async def edit_meeting(self, uow: IUnitOfWork, meeting_id: int, meeting_pd: MeetingsSchemaAdd):
        meeting_dict = meeting_pd.model_dump()
        async with uow:
            try:
                meeting = await uow.meeting.edit_one({'id': meeting_id, 'user_id': uow.current_user.id}, meeting_dict)
                await uow.commit()
            except NoResultFound:
                raise HTTPException(status_code=404, detail="Not found")
            meeting_pd = MeetingsSchema.model_validate(meeting)
            return meeting_pd

    async def delete_meeting(self, uow: IUnitOfWork, meeting_id: int):
        async with uow:
            items = await uow.item.find_all({'meeting_id': meeting_id})
            try:
                await uow.meeting.delete_one({'id': meeting_id, 'user_id': uow.current_user.id})
                await uow.commit()
                self.delete_audio_files([item.audio_record.file_name for item in items])
            except NoResultFound:
                raise HTTPException(status_code=404, detail="Not found")
            return

    async def get_meetings(self, uow: IUnitOfWork):
        async with uow:
            meetings = await uow.meeting.find_all({'user_id': uow.current_user.id})
            meetings_pd_list = [MeetingsSchema(**meeting.__dict__) for meeting in meetings]
            return meetings_pd_list

    @staticmethod
    def delete_audio_files(audio_file_names):
        for audio_file_name in audio_file_names:
            try:
                os.remove(os.path.join(BASE_DIR, 'media', audio_file_name))
            except FileNotFoundError:
                pass



