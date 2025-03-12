"""This module contains APIClient class"""

from typing import List
from abc import ABC, abstractmethod

from app.api.response import LocationDataResponse


class APIClient(ABC):
    """This base class abstracts location data API client methods"""

    @abstractmethod
    async def get(self) -> List[LocationDataResponse]:
        pass
