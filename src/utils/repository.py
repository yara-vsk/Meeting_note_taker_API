from abc import ABC, abstractmethod
from typing import Literal

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, lazyload, joinedload, class_mapper


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
        self.mapper = class_mapper(self.model)

    async def add_one(self, values: dict):
        stmt = insert(self.model).values(**values).returning(self.model)

        for relationship in self.mapper.relationships:
            stmt = stmt.options(selectinload(relationship))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, data: dict):
        stmt1 = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt1)
        stmt2 = delete(self.model).filter_by(**data)
        await self.session.execute(stmt2)
        return res.scalar_one()

    async def edit_one(self, data: dict, values: dict):
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt)
        object_ = res.scalar_one()
        for key, value in values.items():
            setattr(object_, key, value)
        return object_

    async def find_all(self, data: dict = None):
        if not data:
            data = {}
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def find_one(self, data: dict):
        stmt = select(self.model).filter_by(**data)
        res = await self.session.execute(stmt)
        return res.scalar_one()

