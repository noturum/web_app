import os
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (DeclarativeBase,
                            mapped_column, Mapped)


class BaseOrmModel(DeclarativeBase):



    @classmethod
    async def all(cls):
            stmt = select(cls)
            res = await db_controller.execute_stmt(stmt)
            return [user[0] for user in res]

    @classmethod
    async def get_by_id(cls, id_value: Optional[int] = None):
        id_chat = id_value
        stmt = select(cls).where(cls.id == id_chat)
        res = await db_controller.execute_stmt(stmt)
        return res.one_or_none()


    async def save(self):
        async with AsyncSession(db_controller.engine, expire_on_commit=False) as session:
            async with session.begin():
                session.add(self)
            await session.commit()
            id_ = self.id
            await session.close()
            await db_controller.engine.dispose()
        return id_

    async def remove(self):
        async with AsyncSession(db_controller.engine) as session:
            async with session.begin():
                await session.delete(self)
            await session.commit()
            await session.close()
            await db_controller.engine.dispose()


DB = os.getenv('DB_PATH') or "sqlite+aiosqlite:///data.db"


class DataBaseClient:
    __inst__ = None

    def __new__(cls):
        if not cls.__inst__:
            cls.__inst__ = super().__new__(cls)
        return cls.__inst__

    def __init__(self):
        self.engine = create_async_engine(DB)

    async def bootstrap(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseOrmModel.metadata.create_all)

    async def execute_stmt(self, stmt):
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            res = await session.execute(stmt)
            await session.commit()
            await session.close()
            await self.engine.dispose()
        return res


db_controller = DataBaseClient()
