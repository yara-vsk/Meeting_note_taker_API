from src.models.meetings import Meeting
from src.utils.repository import SQLAlchemyRepository


class MeetingsRepository(SQLAlchemyRepository):
    model = Meeting