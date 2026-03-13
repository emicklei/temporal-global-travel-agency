from datetime import date

import airliner.main as main_module
from airliner.main import (
    format_conversion_message,
    format_current_week_dates_message,
    format_current_week_number_message,
    format_scientist_quote_message,
    main,
)


def test_format_conversion_message() -> None:
    assert format_conversion_message(24) == "24 degrees Celsius is 75.2 Fahrenheit"


def test_format_scientist_quote_message(monkeypatch) -> None:
    monkeypatch.setattr(
        main_module,
        "random_scientist_quote",
        lambda: "Somewhere, something incredible is waiting to be known. - Carl Sagan",
    )

    assert (
        format_scientist_quote_message()
        == "Scientist quote: Somewhere, something incredible is waiting to be known. - Carl Sagan"
    )


def test_format_current_week_dates_message(monkeypatch) -> None:
    class FrozenDate(date):
        @classmethod
        def today(cls) -> "FrozenDate":
            return cls(2026, 3, 12)

    monkeypatch.setattr(main_module, "date", FrozenDate)
    converter_calls = []

    def fake_week_number_to_date_range(week_number: int, year: int) -> tuple[date, date]:
        converter_calls.append((week_number, year))
        return date(2026, 3, 9), date(2026, 3, 15)

    monkeypatch.setattr(main_module, "WeekNumberToDateRange", fake_week_number_to_date_range)

    assert (
        format_current_week_dates_message()
        == "Current week dates: 2026-03-09, 2026-03-10, 2026-03-11, 2026-03-12, 2026-03-13, 2026-03-14, 2026-03-15"
    )
    iso_calendar = FrozenDate.today().isocalendar()
    assert converter_calls == [(iso_calendar.week, iso_calendar.year)]


def test_format_current_week_number_message(monkeypatch) -> None:
    class FrozenDate(date):
        @classmethod
        def today(cls) -> "FrozenDate":
            return cls(2026, 3, 12)

    monkeypatch.setattr(main_module, "date", FrozenDate)

    assert format_current_week_number_message() == "Current week number: 11"


def test_main_prints_conversion_and_quote(capsys, monkeypatch) -> None:
    monkeypatch.setattr(
        main_module,
        "random_scientist_quote",
        lambda: "Nothing in life is to be feared, it is only to be understood. - Marie Curie",
    )

    class FrozenDate(date):
        @classmethod
        def today(cls) -> "FrozenDate":
            return cls(2026, 3, 12)

    monkeypatch.setattr(main_module, "date", FrozenDate)
    monkeypatch.setattr(
        main_module,
        "WeekNumberToDateRange",
        lambda week_number, year: (date(2026, 3, 9), date(2026, 3, 15)),
    )

    main()
    captured = capsys.readouterr()
    assert captured.out.strip().splitlines() == [
        "24 degrees Celsius is 75.2 Fahrenheit",
        "Scientist quote: Nothing in life is to be feared, it is only to be understood. - Marie Curie",
        "Current week number: 11",
        "Current week dates: 2026-03-09, 2026-03-10, 2026-03-11, 2026-03-12, 2026-03-13, 2026-03-14, 2026-03-15",
    ]
