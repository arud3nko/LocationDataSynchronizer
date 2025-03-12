"""This module contains APIRepository class"""

from typing import List

from app.api import APIClient
from app.services.api import APIService
from app.core.models import LocationData
from app.core.events import EventManager


class LocationDataAPIService(APIService[LocationData]):
    """
    This class provides methods to interact with concrete `LocationDataAPIClient`.
    This class encapsulates API data validation logic.
    """

    def __init__(self, client: APIClient):
        """
        Construct.

        :param client: `LocationDataAPIClient` instance
        """

        self._client = client

    @EventManager.event("fetch_location_data_api")
    async def get(self) -> List[LocationData]:
        """
        Requests location data from API client & validates response.
        Skips invalid location identifiers.

        :return: List of valid `LocationData` instances
        """

        location_data = await self._client.get()

        location_identifiers = []

        for identifier in location_data:
            try:
                location_identifier = LocationData.model_validate(identifier)
            except ValueError:
                continue
            else:
                location_identifiers.append(location_identifier)

        return location_identifiers
