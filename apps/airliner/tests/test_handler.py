import asyncio
import json
from pathlib import Path
from uuid import UUID

from apis.airliner.v1.flight_plan import FlightPlan
from worker.handler import FlightNexusServiceHandler
from workflows.workflows import RunFlightPlanWorkflow


class _FakeContext:
    def __init__(self, handle):
        self.handle = handle
        self.captured = {}

    async def start_workflow(self, workflow_run, plan, *, id):
        self.captured["workflow_run"] = workflow_run
        self.captured["plan"] = plan
        self.captured["id"] = id
        return self.handle


def _flight_plan_payload() -> dict:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def test_execute_plan_starts_workflow_and_returns_handle(monkeypatch) -> None:
    info_messages = []

    import worker.handler as handler_module

    monkeypatch.setattr(handler_module.logger, "info", lambda msg: info_messages.append(msg))

    plan = FlightPlan(**_flight_plan_payload())
    plan.parent_id = "journey-123"

    handle = object()
    ctx = _FakeContext(handle)

    result = asyncio.run(FlightNexusServiceHandler().execute_plan(ctx, plan))

    assert result is handle
    assert ctx.captured["workflow_run"] is RunFlightPlanWorkflow.run
    assert ctx.captured["plan"] is plan

    workflow_id = ctx.captured["id"]
    assert workflow_id.startswith(f"{plan.id}-workflow-")
    UUID(workflow_id.removeprefix(f"{plan.id}-workflow-"))

    assert info_messages == [
        f"Nexus handler received flight plan={plan.id}, journey={plan.parent_id}"
    ]
