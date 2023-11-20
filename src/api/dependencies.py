from typing import Annotated
from fastapi import Depends
from src.utils.unitofwork import IUnitOfWork, UnitOfWork
from fastapi import HTTPException, UploadFile, Depends


MAX_SIZE = 1024 * 1024 * 10  # 10 megabytes

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


def valid_audio_record(file: UploadFile):
    if not file.content_type in ['audio/ogg', 'audio/mp4']:
        #raise HTTPException(status_code=418, detail="It isn't .ogg or .wav or .mp3.")
        pass
    if file.size > MAX_SIZE:
        raise HTTPException(status_code=419, detail="The file size cannot be greater than 10 megabytes.")
    return file