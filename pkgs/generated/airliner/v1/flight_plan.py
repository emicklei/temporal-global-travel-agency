from __future__ import annotations

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

ICAOCode = str

Timestampz = str


class FlightPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str
    aircraft_id: str
    creation_date: Timestampz
    departure: ICAOCode
    destination: ICAOCode
    estimated_takeoff: Timestampz
    estimated_landing: Timestampz

    @field_validator("creation_date")
    @classmethod
    def _validate_creation_date(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("creation_date must be RFC 3339 date-time") from error
        return value

    @field_validator("departure")
    @classmethod
    def _validate_departure(cls, value: str) -> str:
        if re.fullmatch(r"^[A-Za-z0-9]{4}$", value) is None:
            raise ValueError("departure does not match required pattern")
        return value

    @field_validator("destination")
    @classmethod
    def _validate_destination(cls, value: str) -> str:
        if re.fullmatch(r"^[A-Za-z0-9]{4}$", value) is None:
            raise ValueError("destination does not match required pattern")
        return value

    @field_validator("estimated_takeoff")
    @classmethod
    def _validate_estimated_takeoff(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("estimated_takeoff must be RFC 3339 date-time") from error
        return value

    @field_validator("estimated_landing")
    @classmethod
    def _validate_estimated_landing(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError("estimated_landing must be RFC 3339 date-time") from error
        return value
