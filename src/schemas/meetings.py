from pydantic import BaseModel
from src.schemas.users import UserRead


class MeetingsSchema(BaseModel):
    id: int
    name: str
    user: UserRead

    class Config:
        from_attributes = True


class MeetingsSchemaAdd(BaseModel):
    name: str


class MeetingsSchemaOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
