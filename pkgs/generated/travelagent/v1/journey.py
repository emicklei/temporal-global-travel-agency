from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass(frozen=True)
class Route:
    schema_version: str
    properties: dict[str, Any]

    def __post_init__(self) -> None:
        self.Validate()

    def Validate(self) -> None:
        schema_version_value = self.schema_version
        if schema_version_value is None:
            raise ValueError("schema_version is required and cannot be None")
        if not isinstance(schema_version_value, str):
            raise TypeError("schema_version must be a string")
        properties_value = self.properties
        if properties_value is None:
            raise ValueError("properties is required and cannot be None")
        if not isinstance(properties_value, dict):
            raise TypeError("properties must be an object")

Timestampz = str

@dataclass(frozen=True)
class Journey:
    id: str
    creation_date: Timestampz
    routes: list[Route]

    def __post_init__(self) -> None:
        self.Validate()

    def Validate(self) -> None:
        id_value = self.id
        if id_value is None:
            raise ValueError("id is required and cannot be None")
        if not isinstance(id_value, str):
            raise TypeError("id must be a string")
        creation_date_value = self.creation_date
        if creation_date_value is None:
            raise ValueError("creation_date is required and cannot be None")
        if not isinstance(creation_date_value, str):
            raise TypeError("creation_date must be a string")
        try:
            datetime.fromisoformat(creation_date_value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("creation_date must be RFC 3339 date-time") from error
        routes_value = self.routes
        if routes_value is None:
            raise ValueError("routes is required and cannot be None")
        if not isinstance(routes_value, list):
            raise TypeError("routes must be a list")
        for index, item in enumerate(routes_value):
            if not isinstance(item, Route):
                raise TypeError("routes[{index}] must be Route")
