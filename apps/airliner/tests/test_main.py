import json
from pathlib import Path
import runpy

import pytest  # pants: no-infer-dep
from pydantic import ValidationError  # pants: no-infer-dep
from generated.airliner.v1.flight_plan import FlightPlan
from airliner.main import main


def _flight_plan_payload() -> dict[str, object]:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def test_main_prints_welcome_message(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "welcome to the airliner app!"


def test_main_module_entrypoint_runs_main(capsys) -> None:
    runpy.run_module("airliner.main", run_name="__main__")
    captured = capsys.readouterr()
    assert captured.out.strip() == "welcome to the airliner app!"


def test_flight_plan_from_json_fixture() -> None:
    payload = _flight_plan_payload()

    plan = FlightPlan(**payload)

    assert plan.id == "fp-20260313-001"
    assert plan.departure == "EHAM"
    assert plan.destination == "KJFK"


def test_flight_plan_validates_against_json_schema() -> None:
    """Test that FlightPlan model validates fixture against JSON schema constraints."""
    payload = _flight_plan_payload()

    # Pydantic model_validate enforces schema constraints
    plan = FlightPlan.model_validate(payload)
    model_schema = FlightPlan.model_json_schema()

    assert set(model_schema["properties"].keys()) == {
        "id",
        "aircraft_id",
        "creation_date",
        "departure",
        "destination",
        "estimated_takeoff",
        "estimated_landing",
    }
    assert set(model_schema["required"]) == {
        "id",
        "aircraft_id",
        "creation_date",
        "departure",
        "destination",
        "estimated_takeoff",
        "estimated_landing",
    }
    assert plan.id == payload["id"]


def test_flight_plan_rejects_extra_properties() -> None:
    """Test that model config forbids extra properties (strict schema compliance)."""
    payload = _flight_plan_payload()
    payload["unexpected"] = "value"

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        FlightPlan.model_validate(payload)


def test_flight_plan_rejects_invalid_date_time() -> None:
    payload = _flight_plan_payload()
    payload["creation_date"] = "not-a-timestamp"

    with pytest.raises(ValidationError, match="invalid RFC 3339 date-time"):
        FlightPlan(**payload)


def test_flight_plan_rejects_none_id() -> None:
    payload = _flight_plan_payload()
    payload["id"] = None

    with pytest.raises(ValidationError):
        FlightPlan(**payload)


def test_flight_plan_rejects_non_string_id() -> None:
    payload = _flight_plan_payload()
    payload["id"] = 123

    with pytest.raises(ValidationError):
        FlightPlan(**payload)


def test_flight_plan_rejects_invalid_departure_pattern() -> None:
    payload = _flight_plan_payload()
    payload["departure"] = "AMS"

    with pytest.raises(ValidationError, match="String should match pattern"):
        FlightPlan(**payload)


def test_flight_plan_rejects_non_string_destination() -> None:
    payload = _flight_plan_payload()
    payload["destination"] = 1234

    with pytest.raises(ValidationError):
        FlightPlan(**payload)


def test_flight_plan_rejects_invalid_estimated_landing() -> None:
    payload = _flight_plan_payload()
    payload["estimated_landing"] = "not-a-date"

    with pytest.raises(ValidationError, match="invalid RFC 3339 date-time"):
        FlightPlan(**payload)


def test_flight_plan_rejects_none_aircraft_id() -> None:
    payload = _flight_plan_payload()
    payload["aircraft_id"] = None

    with pytest.raises(ValidationError):
        FlightPlan(**payload)


def test_flight_plan_rejects_non_string_estimated_takeoff() -> None:
    payload = _flight_plan_payload()
    payload["estimated_takeoff"] = 123

    with pytest.raises(ValidationError):
        FlightPlan(**payload)
