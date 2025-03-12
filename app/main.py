"""This module is an application entry point"""

import argparse
import asyncio

from app.config import AppConfiguration, get_app_configuration

from app.api.client import LocationDataAPIClient
from app.services.api import LocationDataAPIService

from app.db.session import create_sessionmaker
from app.db.repositories import LocationDataDBRepository
from app.services.db import LocationDataDBService

from app.core import LocationDataSynchronizerApp
from app.core.events import EventManager

from app.utils.event_logger import EventLogger
from app.utils.logger import create_queue_logger


def configure_app(app_conf: AppConfiguration) -> LocationDataSynchronizerApp:
    """
    Creates required services instances and configures app.

    :param app_conf: `AppConfiguration` instance
    :return: `LocationDataSynchronizerApp` instance.
    """

    api_client = LocationDataAPIClient(
        url=str(app_conf.LOCATION_DATA_ENDPOINT_URL),
        login=app_conf.AUTH_LOGIN,
        password=app_conf.AUTH_PASSWORD.get_secret_value()
    )

    api_service = LocationDataAPIService(client=api_client)

    session = create_sessionmaker(app_conf.engine_url)

    db_service = LocationDataDBService(
        session=session,
        db_repository=LocationDataDBRepository()
    )

    app = LocationDataSynchronizerApp(api_service=api_service, db_service=db_service)

    return app


def main():
    """
    Creates app and configures additional handlers.
    Runs app in scheduled mode inside asyncio event loop.
    """

    parser = argparse.ArgumentParser(description="Location data synchronizer service")
    parser.add_argument(
        "configfile",
        nargs="?",
        type=str,
        default=".env",
        help="Path to application configuration file (default: .env)"
    )

    args = parser.parse_args()

    app_conf = get_app_configuration(args.configfile)

    app = configure_app(app_conf=app_conf)

    app_logger = create_queue_logger("app")
    event_logger = EventLogger(app_logger)

    EventManager.events["fetch_location_data_api"].subscribe(event_logger.log_fetch_location_data_api)
    EventManager.events["sync_db"].subscribe(event_logger.log_sync_db)

    asyncio.run(app.run_scheduled(crontab=app_conf.SCHEDULE))


if __name__ == '__main__':
    main()
