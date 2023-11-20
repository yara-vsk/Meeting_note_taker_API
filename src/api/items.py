from typing import List, Union, Annotated
from fastapi import APIRouter, Response, Depends, Body
from starlette.background import BackgroundTasks

from src.api.dependencies import UOWDep, valid_audio_record
from src.schemas.items import ItemsSchemaAdd, ItemsSchemaOut
from src.services.items import ItemsService

router = APIRouter(
    prefix="/meetings/{meetingID}/items",
    tags=["items"],
)


@router.get("", response_model=List[ItemsSchemaOut])
async def get_items(
        uow: UOWDep
):
    items = await ItemsService().get_items(uow)
    return items


@router.post("", response_model=ItemsSchemaOut)
async def add_item(

        uow: UOWDep,
        back_task: BackgroundTasks,
        description: str | None = Body(max_length=1000),
        audio_file=Depends(valid_audio_record),
):
    item = await ItemsService().add_item(uow, description, audio_file, back_task)
    return item


@router.get("/{id}", response_model=ItemsSchemaOut)
async def get_item(
        id: int,
        uow: UOWDep
):
    item = await ItemsService().get_item(uow, id)
    return item


@router.put("/{id}", response_model=ItemsSchemaOut)
async def edit_item(
        id: int,
        uow: UOWDep,
        item: ItemsSchemaAdd,
):
    item = await ItemsService().edit_item(uow, id, item)
    return item


@router.delete("/{id}", response_model=None)
async def delete_item(
        id: int,
        uow: UOWDep
) -> Response | dict:
    await ItemsService().delete_item(uow, id)
    return {'Status': f"Item id={id} was deleted"}
