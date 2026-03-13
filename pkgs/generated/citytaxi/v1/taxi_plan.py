from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Address:
    street: str
    house_number: str
    city: str
    postal_code: str
    country_code: str

Timestampz = str

@dataclass(frozen=True)
class TaxiPlan:
    id: str
    license_plate: str
    pick_address: Address
    dropoff_address: Address
    estimated_pickup: Timestampz
    estimated_dropoff: Timestampz
