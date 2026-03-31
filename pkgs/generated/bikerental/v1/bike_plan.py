from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

StationCode = str

Timestampz = str

class BikePlan(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str
    bike_id: str
    pickup_station: StationCode
    dropoff_station: StationCode
    estimated_pickup: Timestampz
    estimated_dropoff: Timestampz

    @field_validator("pickup_station")
    @classmethod
    def _validate_pickup_station(cls, value: str) -> str:
        if re.fullmatch(r'^[A-Z0-9][A-Z0-9-]{1,14}[A-Z0-9]$', value) is None:
            raise ValueError("pickup_station does not match required pattern")
        return value

    @field_validator("dropoff_station")
    @classmethod
    def _validate_dropoff_station(cls, value: str) -> str:
        if re.fullmatch(r'^[A-Z0-9][A-Z0-9-]{1,14}[A-Z0-9]$', value) is None:
            raise ValueError("dropoff_station does not match required pattern")
        return value

    @field_validator("estimated_pickup")
    @classmethod
    def _validate_estimated_pickup(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("estimated_pickup must be RFC 3339 date-time") from error
        return value

    @field_validator("estimated_dropoff")
    @classmethod
    def _validate_estimated_dropoff(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("estimated_dropoff must be RFC 3339 date-time") from error
        return value
