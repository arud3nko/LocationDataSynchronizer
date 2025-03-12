"""This module contains `location_data` table declaration and its Row data type"""

from typing import NamedTuple

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    CheckConstraint,
    MetaData
)

metadata = MetaData()

location_data = Table(
    'location_data',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('lac', Integer, nullable=True),
    Column('cellid', Integer, nullable=True),
    Column('eci', Integer, nullable=True),
    Column('note', String(200), nullable=True),

    CheckConstraint(
        '(lac IS NOT NULL AND eci IS NULL) OR '
        '(lac IS NULL AND cellid IS NULL AND eci IS NOT NULL)',
        name='valid_combination_check'
    )
)


class LocationDataRow(NamedTuple):
    """This class describes location_data table row type"""

    id: int | None = None
    lac: int | None = None
    cellid: int | None = None
    eci: int | None = None
    note: str | None = None
