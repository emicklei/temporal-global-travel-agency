import asyncio
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest  # pants: no-infer-dep
from temporalio.testing import WorkflowEnvironment  # pants: no-infer-dep
from temporalio.worker import Worker  # pants: no-infer-dep

from travelagent.workflows import PrintJourneyWorkflow
from generated.travelagent.v1.journey import Journey, Route


@pytest.mark.skip(reason="Test hangs with Temporal environment")
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
                        properties={
                            "id": "taxi-456",
                            "license_plate": "ABC-1234",
                            "pickup_address": {
                                "street": "Via Roma",
                                "house_number": "10",
                                "city": "Rome",
                                "postal_code": "00100",
                                "country_code": "IT",
                            },
                            "dropoff_address": {
                                "street": "Piazza Navona",
                                "house_number": "1",
                                "city": "Rome",
                                "postal_code": "00186",
                                "country_code": "IT",
                            },
                            "estimated_pickup": "2024-03-19T13:00:00Z",
                            "estimated_dropoff": "2024-03-19T13:45:00Z",
                        },
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
