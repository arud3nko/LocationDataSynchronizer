"""This module contains APIService class"""

from typing import Generic, TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar("T")


class APIService(ABC, Generic[T]):
    """This base class abstracts API service methods"""

    @abstractmethod
    async def get(self) -> List[T]:
        pass
