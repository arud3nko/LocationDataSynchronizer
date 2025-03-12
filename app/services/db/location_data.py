"""This module contains LocationDataDBService class"""

from typing import List, Tuple

from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.repositories import DBRepository
from app.db.tables import LocationDataRow
from app.services.db.base import DBService
from app.core.models import LocationData
from app.core.events import EventManager


class LocationDataDBService(DBService[LocationData]):
    """
    This class is a layer between business logic and SQLAlchemy actions & database repository.
    """

    def __init__(
            self,
            db_repository: DBRepository[LocationDataRow],
            session: async_sessionmaker,
    ):
        """
        Construct.

        :param db_repository: Concrete `DBRepository` instance.
        :param session: `async_sessionmaker` instance
        """

        self._db_repository = db_repository
        self._session = session

    @EventManager.event("select_location_data")
    async def get(self) -> List[LocationData]:
        """
        Select all records from location_data.

        :return: List of `LocationData` instances.
        """

        async with self._session() as session:
            rows = await self._db_repository.get(session=session)
            return [self._row_to_model(row) for row in rows]

    @EventManager.event("sync_db")
    async def sync_db(
            self,
            to_insert: List[LocationData],
            to_delete: List[LocationData],
    ) -> Tuple[List[LocationData], List[LocationData]]:
        """
        Inserts & deletes provided location data identifiers.
        Instances, that are being deleted, should contain not-null `id` attribute.

        :param to_insert: List of `LocationData` instances to be inserted
        :param to_delete: List of `LocationData` instances to be deleted
        :return: Tuple, containing list of inserter and list of deleted `LocationData` instances
        """

        async with self._session.begin() as transaction:
            to_insert_rows = [self._model_to_row(model) for model in to_insert]
            to_delete_rows = [self._model_to_row(model) for model in to_delete]

            inserted_rows = await self._db_repository.insert_many(records=to_insert_rows, session=transaction)
            deleted_rows = await self._db_repository.delete_many(records=to_delete_rows, session=transaction)

        return (
            [self._row_to_model(row) for row in inserted_rows],
            [self._row_to_model(row) for row in deleted_rows],
        )

    @staticmethod
    def _model_to_row(model: LocationData) -> LocationDataRow:
        """
        Maps `LocationData` instance to `LocationDataRow` instance.

        :param model: `LocationData` instance
        :return: `LocationDataRow` instance
        """

        return LocationDataRow(
            id=model.id,
            lac=model.lac,
            cellid=model.cellid,
            eci=model.eci,
        )

    @staticmethod
    def _row_to_model(row: LocationDataRow) -> LocationData:
        """
        Maps `LocationDataRow` instance to `LocationData` instance.

        :param row: `LocationDataRow` instance
        :return: `LocationData` instance
        """

        return LocationData(
            id=row.id,
            lac=row.lac,
            cellid=row.cellid,
            eci=row.eci,
        )
