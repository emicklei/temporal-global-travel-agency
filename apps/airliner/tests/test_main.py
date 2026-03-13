import json
from pathlib import Path
import runpy

import pytest  # pants: no-infer-dep
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


def test_flight_plan_rejects_invalid_date_time() -> None:
    payload = _flight_plan_payload()
    payload["creation_date"] = "not-a-timestamp"

    with pytest.raises(ValueError, match="creation_date must be RFC 3339 date-time"):
        FlightPlan(**payload)


def test_flight_plan_rejects_none_id() -> None:
    payload = _flight_plan_payload()
    payload["id"] = None

    with pytest.raises(ValueError, match="id is required and cannot be None"):
        FlightPlan(**payload)


def test_flight_plan_rejects_non_string_id() -> None:
    payload = _flight_plan_payload()
    payload["id"] = 123

    with pytest.raises(TypeError, match="id must be a string"):
        FlightPlan(**payload)


def test_flight_plan_rejects_invalid_departure_pattern() -> None:
    payload = _flight_plan_payload()
    payload["departure"] = "AMS"

    with pytest.raises(ValueError, match="departure does not match required pattern"):
        FlightPlan(**payload)


def test_flight_plan_rejects_non_string_destination() -> None:
    payload = _flight_plan_payload()
    payload["destination"] = 1234

    with pytest.raises(TypeError, match="destination must be a string"):
        FlightPlan(**payload)


def test_flight_plan_rejects_invalid_estimated_landing() -> None:
    payload = _flight_plan_payload()
    payload["estimated_landing"] = "not-a-date"

    with pytest.raises(ValueError, match="estimated_landing must be RFC 3339 date-time"):
        FlightPlan(**payload)


def test_flight_plan_rejects_none_aircraft_id() -> None:
    payload = _flight_plan_payload()
    payload["aircraft_id"] = None

    with pytest.raises(ValueError, match="aircraft_id is required and cannot be None"):
        FlightPlan(**payload)


def test_flight_plan_rejects_non_string_estimated_takeoff() -> None:
    payload = _flight_plan_payload()
    payload["estimated_takeoff"] = 123

    with pytest.raises(TypeError, match="estimated_takeoff must be a string"):
        FlightPlan(**payload)
