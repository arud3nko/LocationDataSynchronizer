"""This module contains LocationDataAPIClient class"""

from typing import List, Any

import aiohttp

from app.api.base import APIClient
from app.api.response import LocationDataResponse


class LocationDataAPIClient(APIClient):
    """This class contains Location Data API client functionality"""

    def __init__(self, url: str, login: str, password: str):
        """
        Construct.

        :param url: Location data API endpoint URL
        :param login: Basic auth login
        :param password: Basic auth password
        """

        self._url = url
        self.__auth = aiohttp.BasicAuth(login=login, password=password)

    async def _get(self, url: str, session: aiohttp.ClientSession) -> Any:
        """
        Make GET request to provided URL within provided session.
        Includes BasicAuth authentication by default.

        :param url: Request URL
        :param session: `ClientSession` instance
        :return: JSON-parsed response
        """

        async with session.get(url=url, auth=self.__auth) as response:
            return await response.json()

    async def get(self) -> List[LocationDataResponse]:
        """
        Fetch location data API and return parsed response.

        :return: List of `LocationDataResponse` instances
        """

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            location_data = await self._get(url=self._url, session=session)
            return [LocationDataResponse(**data) for data in location_data]
