"""This module contains API responses types"""

from typing import NamedTuple


class LocationDataResponse(NamedTuple):
    """Location data endpoint response type"""

    lac: int
    cellid: int
    eci: int
