"""This module contains LocationDataSynchronizerApp class"""

import asyncio

from typing import List, Tuple

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.models import LocationData
from app.services.db import DBService
from app.services.api import APIService


class LocationDataSynchronizerApp:
    """
    This class contains location data core synchronization logic.
    It uses APIService & DBService to interact with API & database.
    Contains main loop, that triggers synchronization method periodically,
    according to provided schedule.
    """

    def __init__(self, api_service: APIService[LocationData], db_service: DBService[LocationData]):
        """
        Construct.

        :param api_service: `APIService` instance
        :param db_service: `DBService` instance
        """

        self._api_service = api_service
        self._db_service = db_service

        self._scheduler = AsyncIOScheduler()

    async def run_scheduled(self, crontab: str = "* * * * *"):
        """
        Configure scheduler due to provided crontab and run scheduler task.
        Target method is `sync_once`.

        :param crontab: Crontab string. Defaults to <At every minute>
        """

        self._scheduler.add_job(self.sync_once, trigger=CronTrigger.from_crontab(crontab))
        self._scheduler.start()

        while True:
            await asyncio.sleep(1)

    async def sync_once(self):
        """
        Requests actual location data from APIService & existing location data from DBService.
        Synchronizes actual & existing location data using `sync_location_data` method.
        Updates location data in database using DBService `sync_db` method.
        """

        api_location_data, db_location_data = await asyncio.gather(
            self._api_service.get(),
            self._db_service.get(),
        )

        to_insert, to_delete = self.sync_location_data(
            actual_data=api_location_data,
            existing_data=db_location_data,
        )

        _inserted, _deleted = await self._db_service.sync_db(to_insert, to_delete)

    @staticmethod
    def sync_location_data(
            actual_data: List[LocationData],
            existing_data: List[LocationData],
    ) -> Tuple[List[LocationData], List[LocationData]]:
        """
        Creates sets from provided lists of existing & actual `LocationData` instances.
        Calculates difference between sets & returns tuple, whose first element is a
        list of brand new `LocationData` instances, and whose second element is a list of
        no longer relevant `LocationData` instances.

        :param actual_data: List of `LocationData` instances
        :param existing_data: List of `LocationData` instances
        :return: A tuple containing list of brand new `LocationData` instances and
        list of obsolete `LocationData` instances
        """

        actual_set = {(item.lac, item.cellid, item.eci) for item in actual_data}
        existing_set = {(item.lac, item.cellid, item.eci) for item in existing_data}

        new_set = actual_set - existing_set
        obvious_set = existing_set - actual_set

        new_data = [data for data in actual_data if (data.lac, data.cellid, data.eci) in new_set]
        obvious_data = [data for data in existing_data if (data.lac, data.cellid, data.eci) in obvious_set]

        return new_data, obvious_data
