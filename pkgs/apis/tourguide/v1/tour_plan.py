from __future__ import annotations

from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, field_validator


Timestampz = Annotated[
    str, Field(description="Timestamp with time zone in RFC 3339 date-time format.")
]


class Address(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    street: str
    house_number: str
    city: str
    postal_code: str
    country_code: str = Field(
        ..., pattern=r"^[A-Z]{2}$", description="ISO 3166-1 alpha-2 country code."
    )


class TourPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str
    tour_id: str
    location: Address
    estimated_start: Timestampz
    estimated_end: Timestampz

    @field_validator("estimated_start", "estimated_end")
    @classmethod
    def _validate_datetime(cls, v):
        if isinstance(v, datetime):
            return v
        if not isinstance(v, str):
            raise TypeError("expected str or datetime for date-time field")
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"invalid RFC 3339 date-time: {v!r}") from exc
        return v
