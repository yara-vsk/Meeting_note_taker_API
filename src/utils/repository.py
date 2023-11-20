from abc import ABC, abstractmethod
from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, lazyload, joinedload


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def edit_one(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, values: dict):
        stmt = insert(self.model).values(**values).returning(self.model).options(selectinload("*"))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, data: dict):
        stmt = delete(self.model).filter_by(**data).returning(self.model).options(selectinload("*"))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, data: dict, values: dict):
        stmt = update(self.model).values(**values).filter_by(**data).returning(self.model).options(selectinload("*"))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, data: dict = None):
        if not data:
            data = {}
        stmt = select(self.model).filter_by(**data).options(selectinload("*"))
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def find_one(self, data: dict):
        stmt = select(self.model).filter_by(**data).options(selectinload("*"))
        res = await self.session.execute(stmt)
        return res.scalar_one()

