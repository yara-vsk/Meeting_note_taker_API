import asyncio

import whisper
from celery import Celery

from src.config import REDIS_HOST, REDIS_PORT
from src.db import async_session_maker
from src.repositories.audiorecords import AudioRecordsRepository

celery_app = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def transcribe_audio(audio_file_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    return result['text']


async def add_audio_note_to_db(audio_record_id, audio_note):
    async with async_session_maker() as session:
        audio_records = AudioRecordsRepository(session)
        await audio_records.edit_one({'id': audio_record_id}, values={'audio_note': str(audio_note)})
        await session.commit()


@celery_app.task
def audio_note_extractor(audio_file_path, audio_record_id):
    audio_note = transcribe_audio(audio_file_path)
    if audio_note is not None:
        asyncio.run(add_audio_note_to_db(audio_record_id, audio_note))
