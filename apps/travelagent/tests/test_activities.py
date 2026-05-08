import asyncio

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService
import activities.activities as activities_module
from activities.activities import call_airliner_nexus_service


def _plan() -> FlightPlan:
    return FlightPlan(
        id="flight-101",
        aircraft_id="A380-123",
        creation_date="2024-03-19T10:00:00Z",
        departure="CDGA",
        destination="ORLY",
        estimated_takeoff="2024-03-19T10:30:00Z",
        estimated_landing="2024-03-19T11:30:00Z",
    )


def test_call_airliner_nexus_service_executes_expected_operation(monkeypatch) -> None:
    captured = {}

    class FakeNexusClient:
        async def execute_operation(
            self, operation, plan, *, schedule_to_close_timeout
        ):
            captured["operation"] = operation
            captured["plan"] = plan
            captured["timeout"] = schedule_to_close_timeout
            return "ok"

    monkeypatch.setattr(
        activities_module.workflow,
        "create_nexus_client",
        lambda *, service, endpoint: FakeNexusClient(),
    )

    plan = _plan()
    result = asyncio.run(call_airliner_nexus_service(plan))

    assert result == "ok"
    assert captured["operation"] is FlightNexusService.execute_plan
    assert captured["plan"] is plan
    assert captured["timeout"].seconds == 10


def test_call_airliner_nexus_service_uses_expected_client_configuration(
    monkeypatch,
) -> None:
    captured = {}

    class FakeNexusClient:
        async def execute_operation(self, *_args, **_kwargs):
            return "ok"

    def fake_create_nexus_client(*, service, endpoint):
        captured["service"] = service
        captured["endpoint"] = endpoint
        return FakeNexusClient()

    monkeypatch.setattr(
        activities_module.workflow,
        "create_nexus_client",
        fake_create_nexus_client,
    )

    asyncio.run(call_airliner_nexus_service(_plan()))

    assert captured["service"] is FlightNexusService
    assert captured["endpoint"] == activities_module.NEXUS_ENDPOINT
