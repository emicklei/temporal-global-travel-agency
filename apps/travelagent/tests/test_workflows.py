import asyncio
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from temporalio.testing import WorkflowEnvironment  # pants: no-infer-dep
from temporalio.worker import Worker  # pants: no-infer-dep

from travelagent.workflows import PrintJourneyWorkflow
from generated.travelagent.v1.journey import Journey, Route


def test_print_journey_workflow_prints_json_to_console(capsys) -> None:
    journey = Journey(
        id="test-journey-1",
        creation_date="2024-03-19T10:00:00Z",
        routes=[
            Route(
                schema_version="airliner/v1",
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
                        schema_version="citytaxi/v2.0",
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
