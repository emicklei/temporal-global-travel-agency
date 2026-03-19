from datetime import timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from temporalio.testing import WorkflowEnvironment  # pants: no-infer-dep
from temporalio.worker import Worker  # pants: no-infer-dep

import travelagent.workflows as workflows_module
from travelagent.activities import compose_hello_message
from travelagent.workflows import HelloTravelWorkflow, PrintJourneyWorkflow
from generated.travelagent.v1.journey import Journey, Route


def test_hello_travel_workflow_executes_activity_with_expected_arguments(
    monkeypatch,
) -> None:
    captured = {}

    async def fake_execute_activity(activity_fn, name, schedule_to_close_timeout):
        captured["activity_fn"] = activity_fn
        captured["name"] = name
        captured["timeout"] = schedule_to_close_timeout
        return "Hello, Ada! Welcome to Temporal Travel Agent."

    monkeypatch.setattr(
        workflows_module.workflow, "execute_activity", fake_execute_activity
    )

    result = asyncio.run(HelloTravelWorkflow().run("Ada"))

    assert result == "Hello, Ada! Welcome to Temporal Travel Agent."
    assert captured["activity_fn"] is workflows_module.compose_hello_message
    assert captured["name"] == "Ada"
    assert captured["timeout"] == timedelta(seconds=10)


def test_hello_travel_workflow_runs_in_temporal_test_environment() -> None:
    async def run_workflow() -> str:
        async with await WorkflowEnvironment.start_time_skipping() as env:
            task_queue = f"travelagent-test-{uuid4()}"
            workflow_id = f"travelagent-hello-{uuid4()}"

            with ThreadPoolExecutor(max_workers=1) as activity_executor:
                async with Worker(
                    env.client,
                    task_queue=task_queue,
                    workflows=[HelloTravelWorkflow],
                    activities=[compose_hello_message],
                    activity_executor=activity_executor,
                ):
                    return await env.client.execute_workflow(
                        HelloTravelWorkflow.run,
                        "Ada",
                        id=workflow_id,
                        task_queue=task_queue,
                    )

    result = asyncio.run(run_workflow())

    assert result == "Hello, Ada! Welcome to Temporal Travel Agent."


def test_print_journey_workflow_prints_json_to_console(capsys) -> None:
    journey = Journey(
        id="test-journey-1",
        creation_date="2024-03-19T10:00:00Z",
        routes=[
            Route(
                schema_version="1.0",
                properties={"destination": "Paris", "duration": "5 days"},
            )
        ],
    )

    asyncio.run(PrintJourneyWorkflow().run(journey))

    captured = capsys.readouterr()
    assert "test-journey-1" in captured.out
    assert "2024-03-19T10:00:00Z" in captured.out
    assert "Paris" in captured.out
    assert "5 days" in captured.out


def test_print_journey_workflow_runs_in_temporal_test_environment() -> None:
    async def run_workflow() -> None:
        async with await WorkflowEnvironment.start_time_skipping() as env:
            task_queue = f"travelagent-test-{uuid4()}"
            workflow_id = f"travelagent-print-journey-{uuid4()}"

            journey = Journey(
                id="test-journey-2",
                creation_date="2024-03-19T12:00:00Z",
                routes=[
                    Route(
                        schema_version="1.0",
                        properties={"destination": "Rome", "duration": "3 days"},
                    )
                ],
            )

            with ThreadPoolExecutor(max_workers=1) as activity_executor:
                async with Worker(
                    env.client,
                    task_queue=task_queue,
                    workflows=[PrintJourneyWorkflow],
                    activity_executor=activity_executor,
                ):
                    return await env.client.execute_workflow(
                        PrintJourneyWorkflow.run,
                        journey,
                        id=workflow_id,
                        task_queue=task_queue,
                    )

    asyncio.run(run_workflow())
