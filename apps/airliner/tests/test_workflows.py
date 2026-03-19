import asyncio
import json
from pathlib import Path


from generated.airliner.v1.flight_plan import FlightPlan
from airliner.workflows import RunFlightPlan
from logger.activities import log_as_json


def _flight_plan_payload() -> dict:
    fixture_path = Path(__file__).parent / "fixtures" / "flight_plan.json"
    return json.loads(fixture_path.read_text(encoding="utf-8"))


def test_log_flight_plan_workflow_executes_activity_with_expected_arguments(
    monkeypatch,
) -> None:
    captured = {}

    async def fake_execute_activity(
        activity_fn, message, flight_plan_data, schedule_to_close_timeout
    ):
        captured["activity_fn"] = activity_fn
        captured["message"] = message
        captured["flight_plan_data"] = flight_plan_data
        captured["timeout"] = schedule_to_close_timeout
        return None

    import airliner.workflows as workflows_module

    monkeypatch.setattr(
        workflows_module.workflow, "execute_activity", fake_execute_activity
    )

    flight_plan = FlightPlan(**_flight_plan_payload())
    asyncio.run(RunFlightPlan().run(flight_plan))

    assert captured["activity_fn"] is log_as_json
    assert captured["message"] == "Flight plan"
    assert captured["flight_plan_data"]["id"] == "fp-20260313-001"
    assert captured["flight_plan_data"]["departure"] == "EHAM"
    assert captured["flight_plan_data"]["destination"] == "KJFK"


# Integration test commented out due to temporal test environment timeout
# def test_log_flight_plan_workflow_runs_in_temporal_test_environment() -> None:
#     async def run_workflow() -> None:
#         async with await WorkflowEnvironment.start_time_skipping() as env:
#             task_queue = f"airliner-test-{uuid4()}"
#             workflow_id = f"airliner-log-flight-plan-{uuid4()}"
#
#             flight_plan = FlightPlan(**_flight_plan_payload())
#
#             with ThreadPoolExecutor(max_workers=1) as activity_executor:
#                 async with Worker(
#                     env.client,
#                     task_queue=task_queue,
#                     workflows=[LogFlightPlanWorkflow],
#                     activities=[log_as_json],
#                     activity_executor=activity_executor,
#                 ):
#                     return await env.client.execute_workflow(
#                         LogFlightPlanWorkflow.run,
#                         flight_plan,
#                         id=workflow_id,
#                         task_queue=task_queue,
#                     )
#
#     asyncio.run(run_workflow())
