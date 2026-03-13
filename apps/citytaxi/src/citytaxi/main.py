from datetime import date, timedelta

from converters import DegreesToFahrenheit, WeekNumberToDateRange


def format_conversion_message(degrees_celsius: float) -> str:
    fahrenheit = DegreesToFahrenheit(degrees_celsius)
    return f"{degrees_celsius} degrees Celsius is {fahrenheit} Fahrenheit"


def format_current_week_dates_message() -> str:
    today = date.today()
    iso_calendar = today.isocalendar()
    start_of_week, end_of_week = WeekNumberToDateRange(iso_calendar.week, iso_calendar.year)
    week_dates = [
        start_of_week + timedelta(days=offset)
        for offset in range((end_of_week - start_of_week).days + 1)
    ]
    formatted_dates = ", ".join(d.isoformat() for d in week_dates)
    return f"Current week dates: {formatted_dates}"


def format_current_week_number_message() -> str:
    today = date.today()
    iso_calendar = today.isocalendar()
    return f"Current week number: {iso_calendar.week}"


def main() -> None:
    print(format_conversion_message(24))
    print(format_current_week_number_message())
    print(format_current_week_dates_message())


if __name__ == "__main__":
    main()
