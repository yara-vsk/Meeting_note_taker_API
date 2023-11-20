from typing import List
from fastapi import APIRouter, Response
from src.api.dependencies import UOWDep
from src.schemas.meetings import MeetingsSchemaAdd, MeetingsSchema
from src.services.meetings import MeetingsService

router = APIRouter(
    prefix="/meetings",
    tags=["meetings"],
)


@router.get("", response_model=List[MeetingsSchema])
async def get_meetings(
        uow: UOWDep
):
    meetings = await MeetingsService().get_meetings(uow)
    return meetings


@router.post("", response_model=MeetingsSchema)
async def add_meeting(
        uow: UOWDep,
        meeting_pd: MeetingsSchemaAdd
):
    meeting = await MeetingsService().add_meeting(uow, meeting_pd)
    return meeting


@router.get("/{id}", response_model=MeetingsSchema)
async def get_meeting(
        id: int,
        uow: UOWDep
):
    meeting = await MeetingsService().get_meeting(uow, id)
    return meeting


@router.put("/{id}", response_model=MeetingsSchema)
async def edit_meeting(
        id: int,
        meeting_pd: MeetingsSchemaAdd,
        uow: UOWDep
):
    meeting = await MeetingsService().edit_meeting(uow, id, meeting_pd)
    return meeting


@router.delete("/{id}", response_model=None)
async def delete_meeting(
        id: int,
        uow: UOWDep
) -> Response | dict:
    await MeetingsService().delete_meeting(uow, id)
    return {'Status': f"Meeting id={id} was deleted"}
