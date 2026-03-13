from datetime import date

from converters import DegreesToFahrenheit, WeekNumberToDateRange


def test_degrees_to_fahrenheit() -> None:
    assert DegreesToFahrenheit(24) == 75.2


def test_week_number_to_date_range_returns_iso_week_bounds() -> None:
    begin_date, end_date = WeekNumberToDateRange(1, 2026)

    assert begin_date == date(2025, 12, 29)
    assert end_date == date(2026, 1, 4)


def test_week_number_to_date_range_allows_week_53_when_valid() -> None:
    begin_date, end_date = WeekNumberToDateRange(53, 2020)

    assert begin_date == date(2020, 12, 28)
    assert end_date == date(2021, 1, 3)


def test_week_number_to_date_range_rejects_invalid_week_number() -> None:
    try:
        WeekNumberToDateRange(54, 2026)
    except ValueError as exc:
        assert str(exc) == "Invalid ISO week number 54 for year 2026."
    else:
        raise AssertionError("Expected ValueError for invalid week number")
