from __future__ import annotations

from dataclasses import dataclass
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
