from typing import Union

from pydantic import BaseModel, Field
from datetime import datetime

from src.schemas.meetings import MeetingsSchemaOut, MeetingsSchema


class AudioRecordsSchema(BaseModel):
    id: int
    audio_note: Union[str, None] = Field(max_length=1000)
    file_name: str = Field(max_length=500)

    class Config:
        from_attributes = True


class AudioRecordsSchemaAdd(BaseModel):
    file_name: str = Field(max_length=500)


class ItemsSchema(BaseModel):
    id: int
    audio_id: int
    description: Union[str, None] = Field(max_length=1000)
    create_date: datetime

    class Config:
        from_attributes = True


class ItemsSchemaAdd(BaseModel):
    description: Union[str, None]


class ItemsSchemaOut(BaseModel):
    id: int
    description: Union[str, None]
    create_date: datetime
    audio_record: AudioRecordsSchema
    meeting: MeetingsSchema