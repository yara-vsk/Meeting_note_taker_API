from abc import ABC, abstractmethod

from typing import Type, Annotated

from fastapi import Depends, Path
from starlette.requests import Request

from src.db import async_session_maker
from src.models.users import User
from src.repositories.audiorecords import AudioRecordsRepository
from src.repositories.items import ItemsRepository
from src.repositories.meetings import MeetingsRepository
from src.utils.auth_manager import current_active_user


class IUnitOfWork(ABC):
    item: Type[ItemsRepository]
    audio_record: Type[AudioRecordsRepository]
    meeting: Type[MeetingsRepository]
    current_user: User
    current_meeting_id: int

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def rollback(self):
        ...

    @abstractmethod
    async def commit(self):
        ...


class UnitOfWork(IUnitOfWork):

    def __init__(self,
                 request: Request,
                 user: User = Depends(current_active_user)):
        self.session_factory = async_session_maker
        self.current_user = user
        self.current_meeting_id = request.path_params.get('meetingID')


    async def __aenter__(self):
        self.session = self.session_factory()
        self.item = ItemsRepository(self.session)
        self.audio_record = AudioRecordsRepository(self.session)
        self.meeting = MeetingsRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()