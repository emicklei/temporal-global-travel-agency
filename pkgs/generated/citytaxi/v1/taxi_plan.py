from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass(frozen=True)
class Address:
    street: str
    house_number: str
    city: str
    postal_code: str
    country_code: str

    def __post_init__(self) -> None:
        street_value = self.street
        if street_value is None:
            raise ValueError("street is required and cannot be None")
        if not isinstance(street_value, str):
            raise TypeError("street must be a string")
        house_number_value = self.house_number
        if house_number_value is None:
            raise ValueError("house_number is required and cannot be None")
        if not isinstance(house_number_value, str):
            raise TypeError("house_number must be a string")
        city_value = self.city
        if city_value is None:
            raise ValueError("city is required and cannot be None")
        if not isinstance(city_value, str):
            raise TypeError("city must be a string")
        postal_code_value = self.postal_code
        if postal_code_value is None:
            raise ValueError("postal_code is required and cannot be None")
        if not isinstance(postal_code_value, str):
            raise TypeError("postal_code must be a string")
        country_code_value = self.country_code
        if country_code_value is None:
            raise ValueError("country_code is required and cannot be None")
        if not isinstance(country_code_value, str):
            raise TypeError("country_code must be a string")
        if re.fullmatch(r'^[A-Z]{2}$', country_code_value) is None:
            raise ValueError("country_code does not match required pattern")

Timestampz = str

@dataclass(frozen=True)
class TaxiPlan:
    id: str
    license_plate: str
    pick_address: Address
    dropoff_address: Address
    estimated_pickup: Timestampz
    estimated_dropoff: Timestampz

    def __post_init__(self) -> None:
        id_value = self.id
        if id_value is None:
            raise ValueError("id is required and cannot be None")
        if not isinstance(id_value, str):
            raise TypeError("id must be a string")
        license_plate_value = self.license_plate
        if license_plate_value is None:
            raise ValueError("license_plate is required and cannot be None")
        if not isinstance(license_plate_value, str):
            raise TypeError("license_plate must be a string")
        pick_address_value = self.pick_address
        if pick_address_value is None:
            raise ValueError("pick_address is required and cannot be None")
        if not isinstance(pick_address_value, Address):
            raise TypeError("pick_address must be Address")
        dropoff_address_value = self.dropoff_address
        if dropoff_address_value is None:
            raise ValueError("dropoff_address is required and cannot be None")
        if not isinstance(dropoff_address_value, Address):
            raise TypeError("dropoff_address must be Address")
        estimated_pickup_value = self.estimated_pickup
        if estimated_pickup_value is None:
            raise ValueError("estimated_pickup is required and cannot be None")
        if not isinstance(estimated_pickup_value, str):
            raise TypeError("estimated_pickup must be a string")
        try:
            datetime.fromisoformat(estimated_pickup_value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("estimated_pickup must be RFC 3339 date-time") from error
        estimated_dropoff_value = self.estimated_dropoff
        if estimated_dropoff_value is None:
            raise ValueError("estimated_dropoff is required and cannot be None")
        if not isinstance(estimated_dropoff_value, str):
            raise TypeError("estimated_dropoff must be a string")
        try:
            datetime.fromisoformat(estimated_dropoff_value.replace('Z', '+00:00'))
        except ValueError as error:
            raise ValueError("estimated_dropoff must be RFC 3339 date-time") from error
