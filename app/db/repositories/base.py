"""This module contains BaseRepository class"""

from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class DBRepository(ABC, Generic[T]):
    """This base class describes abstract repository methods"""

    @abstractmethod
    async def get(self, session: AsyncSession) -> List[T]:
        pass

    @abstractmethod
    async def insert_many(self, records: List[T], session: AsyncSession) -> List[T]:
        pass

    @abstractmethod
    async def delete_many(self, records: List[T], session: AsyncSession) -> List[T]:
        pass
