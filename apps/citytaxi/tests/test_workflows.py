import asyncio
import json
from pathlib import Path


from apis.citytaxi.v1.taxi_plan import TaxiPlan
from workflows.workflows import RunTaxiPlanWorkflow
from logger.activities import log_as_json


def _taxi_plan_payload() -> dict:
    fixture_path = Path(__file__).parent / "fixtures" / "taxi_plan.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def test_log_taxi_plan_workflow_executes_activity_with_expected_arguments(
    monkeypatch,
) -> None:
    captured = {}

    async def fake_execute_activity(activity_fn, *, args, schedule_to_close_timeout):
        captured["activity_fn"] = activity_fn
        captured["message"] = args[0]
        captured["taxi_plan_data"] = args[1]
        captured["timeout"] = schedule_to_close_timeout
        return None

    import workflows.workflows as workflows_module

    monkeypatch.setattr(
        workflows_module.workflow, "execute_activity", fake_execute_activity
    )

    taxi_plan = TaxiPlan(**_taxi_plan_payload())
    asyncio.run(RunTaxiPlanWorkflow().run(taxi_plan))

    assert captured["activity_fn"] is log_as_json
    assert captured["message"] == "Taxi plan"
    assert captured["taxi_plan_data"]["id"] == "tp-20260313-001"
    assert captured["taxi_plan_data"]["license_plate"] == "TX-123-AB"
