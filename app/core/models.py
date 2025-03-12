"""This module contains app business-models and validation functionality"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, model_validator, AfterValidator


def is_lac_valid(value: int | None) -> int | None:
    """Check if lac value is within specified range"""

    if value is None or 0 < value < 0xFFFF:
        return value

    raise ValueError


def is_cellid_valid(value: int | None) -> int | None:
    """Check if cellid value is within specified range"""

    if value is None or 0 < value < 0xFFFF:
        return value

    raise ValueError


def is_eci_valid(value: int | None) -> int | None:
    """Check if eci value is within specified range"""

    if value is None or 0 < value < 0xFFFFFFF:
        return value

    raise ValueError


class LocationData(BaseModel):
    """This model describes location identifier fields & their validation"""

    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    lac: Annotated[int | None, AfterValidator(is_lac_valid)]
    cellid: Annotated[int | None, AfterValidator(is_cellid_valid)]
    eci: Annotated[int | None, AfterValidator(is_eci_valid)]

    @model_validator(mode="after")
    def validate_identifier_combinations(self):
        """Ensure valid combinations of location identifiers."""

        has_lac = self.lac is not None
        has_cellid = self.cellid is not None
        has_eci = self.eci is not None

        if has_eci and (has_lac or has_cellid):
            raise ValueError("If 'eci' is provided, 'lac' and 'cellid' must be None.")

        if not has_eci and not has_lac:
            raise ValueError("Valid combinations are: 'lac', 'lac + cellid', or 'eci'.")

        return self
