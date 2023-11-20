from sqlalchemy import select

from src.models.items import Item
from src.utils.repository import SQLAlchemyRepository


class ItemsRepository(SQLAlchemyRepository):
    model = Item