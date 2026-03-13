from datetime import date


def DegreesToFahrenheit(degrees_celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (degrees_celsius * 9 / 5) + 32


def WeekNumberToDateRange(week_number: int, year: int | None = None) -> tuple[date, date]:
    """Return the ISO week start (Monday) and end (Sunday) dates."""
    if year is None:
        year = date.today().year

    try:
        begin_date = date.fromisocalendar(year, week_number, 1)
    except ValueError as exc:
        raise ValueError(
            f"Invalid ISO week number {week_number} for year {year}."
        ) from exc

    end_date = date.fromisocalendar(year, week_number, 7)
    return begin_date, end_date
