import json
from pathlib import Path

from apis.travelagent.v1.journey import Journey


def test_creates_and_validates_journey_from_plan_fixture() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "plan1.json"
    fixture_payload = json.loads(fixture_path.read_text(encoding="utf-8"))

    journey_payload = {
        "id": fixture_payload["id"],
        "creation_date": fixture_payload["routes"][0]["properties"]["creation_date"],
        "routes": fixture_payload["routes"],
    }

    journey = Journey.model_validate(journey_payload)

    assert journey.id == "plan1"
    assert journey.creation_date == "2026-03-13T09:30:00Z"
    assert len(journey.routes) == 3
    assert journey.routes[0].schema_version == "airliner/v1"
    assert journey.routes[1].schema_version == "citytaxi/v1"
    assert journey.routes[2].schema_version == "bikerental/v1"
