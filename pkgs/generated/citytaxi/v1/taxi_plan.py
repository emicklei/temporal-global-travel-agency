from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

class Address(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    street: str
    house_number: str
    city: str
    postal_code: str
    country_code: str

    @field_validator("country_code")
    @classmethod
    def _validate_country_code(cls, value: str) -> str:
        if re.fullmatch(r'^[A-Z]{2}$', value) is None:
            raise ValueError("country_code does not match required pattern")
        return value

Timestampz = str

class TaxiPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str
    license_plate: str
    pickup_address: Address
    dropoff_address: Address
    estimated_pickup: Timestampz
    estimated_dropoff: Timestampz

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
