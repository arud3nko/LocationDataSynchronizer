"""This module provides configurations"""

from functools import lru_cache

from sqlalchemy.engine import URL

from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, DotEnvSettingsSource


class AppConfiguration(BaseSettings):
    """This model contains common app configurations"""

    LOCATION_DATA_ENDPOINT_URL: HttpUrl
    AUTH_LOGIN: str
    AUTH_PASSWORD: SecretStr
    SCHEDULE: str

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def engine_url(self):
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
            query={},
        )


@lru_cache
def get_app_configuration(path: str) -> AppConfiguration:
    """Cached AppConfiguration getter"""

    source = DotEnvSettingsSource(AppConfiguration, env_file=path)
    return AppConfiguration.model_validate(source())
