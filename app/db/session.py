"""This module provides async session fabric"""

from sqlalchemy.engine import URL

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


def create_sessionmaker(engine_url: URL) -> async_sessionmaker:
    """
    Creates async engine with provided URL and async sessionmaker with created engine.

    :param engine_url: DB engine URL
    :return: `async_sessionmaker` instance
    """

    engine = create_async_engine(
        url=engine_url
    )

    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
