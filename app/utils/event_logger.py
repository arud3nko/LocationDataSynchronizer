"""This module contains EventLogger class"""

from logging import DEBUG, INFO, WARNING, ERROR, Logger
from typing import List, Tuple

from app.core.models import LocationData


class EventLogger:
    """
    This class is a facade for pre-defined event logging methods.
    EventLogger requires logger instance to be used.
    """

    def __init__(self, logger: Logger):
        """
        Construct.

        :param logger: `Logger` instance
        """

        self._logger = logger

    def _log_location_data(
            self,
            location_data: LocationData,
            level: DEBUG | INFO | WARNING | ERROR = INFO,
            message: str | None = "",
    ):
        """
        Creates formatted message and sends it into logger.

        :param location_data: `LocationData` instance
        :param level: Logging level
        :param message: Optional message to be added before instance representation
        """

        message = f"{message} {location_data}"
        self._logger.log(level=level, msg=message)

    def log_sync_db(self, updated_data: Tuple[List[LocationData], List[LocationData]]):
        """Log sync_db event"""

        inserted, deleted = updated_data

        for identifier in inserted:
            self._log_location_data(identifier, message="INSERT")
        for identifier in deleted:
            self._log_location_data(identifier, message="DELETE")

    def log_fetch_location_data_api(self, received_data: List[LocationData]):
        """Log fetch_location_data_api event"""

        self._logger.info(f"Fetched API. Received {len(received_data)} location data identifiers")
