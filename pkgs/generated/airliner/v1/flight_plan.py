from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

ICAOCode = str

Timestampz = str

@dataclass(frozen=True)
class FlightPlan:
    id: str
    aircraft_id: str
    creation_date: Timestampz
    departure: ICAOCode
    destination: ICAOCode
    estimated_takeoff: Timestampz
    estimated_landing: Timestampz

    def __post_init__(self) -> None:
        id_value = self.id
        if id_value is None:
            raise ValueError("id is required and cannot be None")
        if not isinstance(id_value, str):
            raise TypeError("id must be a string")
        aircraft_id_value = self.aircraft_id
        if aircraft_id_value is None:
            raise ValueError("aircraft_id is required and cannot be None")
        if not isinstance(aircraft_id_value, str):
            raise TypeError("aircraft_id must be a string")
        creation_date_value = self.creation_date
        if creation_date_value is None:
            raise ValueError("creation_date is required and cannot be None")
        if not isinstance(creation_date_value, str):
            raise TypeError("creation_date must be a string")
        try:
            datetime.fromisoformat(creation_date_value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("creation_date must be RFC 3339 date-time") from error
        departure_value = self.departure
        if departure_value is None:
            raise ValueError("departure is required and cannot be None")
        if not isinstance(departure_value, str):
            raise TypeError("departure must be a string")
        if re.fullmatch(r'^[A-Za-z0-9]{4}$', departure_value) is None:
            raise ValueError("departure does not match required pattern")
        destination_value = self.destination
        if destination_value is None:
            raise ValueError("destination is required and cannot be None")
        if not isinstance(destination_value, str):
            raise TypeError("destination must be a string")
        if re.fullmatch(r'^[A-Za-z0-9]{4}$', destination_value) is None:
            raise ValueError("destination does not match required pattern")
        estimated_takeoff_value = self.estimated_takeoff
        if estimated_takeoff_value is None:
            raise ValueError("estimated_takeoff is required and cannot be None")
        if not isinstance(estimated_takeoff_value, str):
            raise TypeError("estimated_takeoff must be a string")
        try:
            datetime.fromisoformat(estimated_takeoff_value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("estimated_takeoff must be RFC 3339 date-time") from error
        estimated_landing_value = self.estimated_landing
        if estimated_landing_value is None:
            raise ValueError("estimated_landing is required and cannot be None")
        if not isinstance(estimated_landing_value, str):
            raise TypeError("estimated_landing must be a string")
        try:
            datetime.fromisoformat(estimated_landing_value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("estimated_landing must be RFC 3339 date-time") from error
