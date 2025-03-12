"""This module contains Location Data repository"""

from typing import List
from itertools import batched

from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.base import DBRepository
from app.db.tables import location_data, LocationDataRow

_BATCH_SIZE = 10_000


class LocationDataDBRepository(DBRepository[LocationDataRow]):
    """
    LocationData repository provides functionality for interacting with the database.

    This repository is built using classic **imperative** style. There are some reasons for
    this decision:

    - Interactions with database should be optimized due to required mass data insertion & deletion.
    - Full control over statements creation and its execution. Using bulk delete & insert is much faster
      than inserting over Unit of Work ORM pattern.
    - Using ORM mapping models degrades performance significantly due to its identity mapping.
    """

    async def get(self, session: AsyncSession) -> List[LocationDataRow]:
        """
        Get all records from location_data table & return LocationData instances.

        :param session: `AsyncSession` instance
        :return: List of `LocationDataRow` instances
        """

        records = await session.execute(select(location_data))
        data = [LocationDataRow(*record) for record in records.all()]

        return data

    async def insert_many(self, records: List[LocationDataRow], session: AsyncSession) -> List[LocationDataRow]:
        """
        Insert many records.
        Maps `LocationData` instances to batched list of values dicts.
        Executes insert statements with values from batches.

        :param records: List of `LocationData` instances
        :param session: `AsyncSession` instance
        :return: List of inserted `LocationData` instances
        """

        values = [{"lac": record.lac, "cellid": record.cellid, "eci": record.eci} for record in records]
        batched_values = batched(values, _BATCH_SIZE)

        inserted_records = []

        for batch in batched_values:
            stmt = insert(location_data).returning(location_data)
            result = await session.execute(stmt, batch)
            inserted_records.extend(result.all())

        return [LocationDataRow(*record) for record in inserted_records]

    async def delete_many(self, records: List[LocationDataRow], session: AsyncSession) -> List[LocationDataRow]:
        """
        Delete many records.
        Maps `LocationData` instances to list of ids, which records will be removed.
        Executes delete statements with values from batches.

        :param records: List of `LocationData` instances
        :param session: `AsyncSession` instance
        :return: List of deleted `LocationData` instances
        """

        ids = [record.id for record in records if record.id is not None]
        batched_ids = batched(ids, _BATCH_SIZE)

        removed_records = []

        for batch in batched_ids:
            stmt = delete(location_data).returning(location_data).where(location_data.c.id.in_(batch))
            result = await session.execute(stmt)
            removed_records.extend(result.all())

        return [LocationDataRow(*record) for record in removed_records]
