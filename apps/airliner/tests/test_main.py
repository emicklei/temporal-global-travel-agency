from datetime import date
import json
from pathlib import Path

import converters
from generated.airliner.v1.flight_plan import FlightPlan
import quotes
from airliner.main import main


def test_main_prints_flight_plan(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "Flight Plan: FlightPlan(id='fp-20260313-001', aircraft_id='A320-NEO-42', creation_date='2026-03-13T09:30:00Z', departure='EHAM', destination='KJFK', estimated_takeoff='2026-03-13T10:15:00Z', estimated_landing='2026-03-13T17:05:00Z')",
    ]


def test_flight_plan_from_json_fixture() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))

    plan = FlightPlan(**payload)

    assert plan.id == "fp-20260313-001"
    assert plan.departure == "EHAM"
    assert plan.destination == "KJFK"


def test_flight_plan_rejects_invalid_date_time() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    payload["creation_date"] = "not-a-timestamp"

    try:
        FlightPlan(**payload)
    except ValueError as exc:
        assert str(exc) == "creation_date must be RFC 3339 date-time"
    else:
        raise AssertionError("Expected ValueError for invalid creation_date")


def test_flight_plan_rejects_invalid_departure_pattern() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    payload["departure"] = "AMS"

    try:
        FlightPlan(**payload)
    except ValueError as exc:
        assert str(exc) == "departure does not match required pattern"
    else:
        raise AssertionError("Expected ValueError for invalid departure")


def test_flight_plan_rejects_non_string_destination() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    payload["destination"] = 1234

    try:
        FlightPlan(**payload)
    except TypeError as exc:
        assert str(exc) == "destination must be a string"
    else:
        raise AssertionError("Expected TypeError for non-string destination")


def test_flight_plan_rejects_invalid_estimated_landing() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    payload["estimated_landing"] = "not-a-date"

    try:
        FlightPlan(**payload)
    except ValueError as exc:
        assert str(exc) == "estimated_landing must be RFC 3339 date-time"
    else:
        raise AssertionError("Expected ValueError for invalid estimated_landing")


def test_flight_plan_rejects_none_aircraft_id() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    payload["aircraft_id"] = None

    try:
        FlightPlan(**payload)
    except ValueError as exc:
        assert str(exc) == "aircraft_id is required and cannot be None"
    else:
        raise AssertionError("Expected ValueError for missing aircraft_id")


def test_flight_plan_rejects_non_string_estimated_takeoff() -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    payload["estimated_takeoff"] = 123

    try:
        FlightPlan(**payload)
    except TypeError as exc:
        assert str(exc) == "estimated_takeoff must be a string"
    else:
        raise AssertionError("Expected TypeError for non-string estimated_takeoff")


def test_week_number_to_date_range_returns_iso_week_bounds() -> None:
    begin_date, end_date = converters.WeekNumberToDateRange(1, 2026)

    assert begin_date == date(2025, 12, 29)
    assert end_date == date(2026, 1, 4)


def test_week_number_to_date_range_rejects_invalid_week_number() -> None:
    try:
        converters.WeekNumberToDateRange(54, 2026)
    except ValueError as exc:
        assert str(exc) == "Invalid ISO week number 54 for year 2026."
    else:
        raise AssertionError("Expected ValueError for invalid week number")


def test_week_number_to_date_range_uses_current_year(monkeypatch) -> None:
    class FrozenDate(date):
        @classmethod
        def today(cls) -> "FrozenDate":
            return cls(2026, 2, 2)

    monkeypatch.setattr(converters, "date", FrozenDate)

    begin_date, end_date = converters.WeekNumberToDateRange(6)

    assert begin_date == date(2026, 2, 2)
    assert end_date == date(2026, 2, 8)


def test_random_scientist_quote_uses_quotes_collection(monkeypatch) -> None:
    monkeypatch.setattr(quotes, "choice", lambda items: items[0])

    assert (
        quotes.random_scientist_quote()
        == "Somewhere, something incredible is waiting to be known. - Carl Sagan"
    )
