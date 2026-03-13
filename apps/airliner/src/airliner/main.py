from generated.airliner.v1.flight_plan import FlightPlan


def main() -> None:
    plan = FlightPlan(
        id="fp-20260313-001",
        aircraft_id="A320-NEO-42",
        creation_date="2026-03-13T09:30:00Z",
        departure="EHAM",
        destination="KJFK",
        estimated_takeoff="2026-03-13T10:15:00Z",
        estimated_landing="2026-03-13T17:05:00Z",
    )
    print("Flight Plan:", plan)


if __name__ == "__main__":
    main()
