"""This module contains DBService class"""

from typing import Generic, TypeVar, List, Tuple
from abc import ABC, abstractmethod

T = TypeVar("T")


class DBService(ABC, Generic[T]):
    """This base class abstracts DB service methods"""

    @abstractmethod
    async def get(self) -> List[T]:
        pass

    @abstractmethod
    async def sync_db(self, to_insert: List[T], to_delete: List[T]) -> Tuple[List[T], List[T]]:
        pass
