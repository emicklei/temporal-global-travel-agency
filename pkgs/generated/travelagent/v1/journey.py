from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

class Route(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    schema_version: str
    properties: dict[str, Any]

    @field_validator("schema_version")
    @classmethod
    def _validate_schema_version(cls, value: str) -> str:
        if re.fullmatch(r'^[^/]+/v[0-9]+(?:[.][0-9]+)*$', value) is None:
            raise ValueError("schema_version does not match required pattern")
        return value

Timestampz = str

class Journey(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    id: str
    creation_date: Timestampz
    routes: list[Route]

    @field_validator("creation_date")
    @classmethod
    def _validate_creation_date(cls, value: str) -> str:
        try:
            datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("creation_date must be RFC 3339 date-time") from error
        return value
