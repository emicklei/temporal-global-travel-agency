import asyncio
import json
from pathlib import Path


from apis.bikerental.v1.bike_plan import BikePlan
from workflows.workflows import RunBikePlanWorkflow
from logger.activities import log_as_json


def _bike_plan_payload() -> dict:
    fixture_path = Path(__file__).parent / "fixtures" / "bike_plan.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def test_log_bike_plan_workflow_executes_activity_with_expected_arguments(
    monkeypatch,
) -> None:
    captured = {}

    async def fake_execute_activity(activity_fn, *, args, schedule_to_close_timeout):
        captured["activity_fn"] = activity_fn
        captured["message"] = args[0]
        captured["bike_plan_data"] = args[1]
        captured["timeout"] = schedule_to_close_timeout
        return None

    import workflows.workflows as workflows_module

    monkeypatch.setattr(
        workflows_module.workflow, "execute_activity", fake_execute_activity
    )
    monkeypatch.setattr(workflows_module.workflow.logger, "info", lambda _msg: None)

    bike_plan = BikePlan(**_bike_plan_payload())
    asyncio.run(RunBikePlanWorkflow().run(bike_plan))

    assert captured["activity_fn"] is log_as_json
    assert captured["message"] == "Bike plan"
    assert captured["bike_plan_data"]["id"] == "bp-20260313-001"
    assert captured["bike_plan_data"]["bike_id"] == "bike-123"
