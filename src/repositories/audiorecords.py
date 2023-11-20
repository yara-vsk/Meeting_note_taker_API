from src.models.items import AudioRecord
from src.utils.repository import SQLAlchemyRepository


class AudioRecordsRepository(SQLAlchemyRepository):
    model = AudioRecord