import asyncio
import json
from pathlib import Path


from apis.tourguide.v1.tour_plan import TourPlan
from workflows.workflows import RunTourPlanWorkflow
from logger.activities import log_as_json


def _tour_plan_payload() -> dict:
    fixture_path = Path(__file__).parent / "fixtures" / "tour_plan.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def test_log_tour_plan_workflow_executes_activity_with_expected_arguments(
    monkeypatch,
) -> None:
    captured = {}

    async def fake_execute_activity(activity_fn, *, args, schedule_to_close_timeout):
        captured["activity_fn"] = activity_fn
        captured["message"] = args[0]
        captured["tour_plan_data"] = args[1]
        captured["timeout"] = schedule_to_close_timeout
        return None

    import workflows.workflows as workflows_module

    monkeypatch.setattr(
        workflows_module.workflow, "execute_activity", fake_execute_activity
    )

    tour_plan = TourPlan(**_tour_plan_payload())
    asyncio.run(RunTourPlanWorkflow().run(tour_plan))

    assert captured["activity_fn"] is log_as_json
    assert captured["message"] == "Tour plan"
    assert captured["tour_plan_data"]["id"] == "tgp-20260313-001"
    assert captured["tour_plan_data"]["tour_id"] == "tour-456"
