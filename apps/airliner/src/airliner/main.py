from generated.airliner.v1.flight_plan import FlightPlan
from logger import LogRecord, append_log_record


def main() -> None:
    message = "welcome to the airliner app!"
    print(message)
    append_log_record(
        "airliner.log",
        LogRecord(level="INFO", message=message, logger_name="airliner"),
    )


if __name__ == "__main__":
    main()
