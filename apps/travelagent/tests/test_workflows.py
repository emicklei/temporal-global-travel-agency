import asyncio
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest  # pants: no-infer-dep
from temporalio.testing import WorkflowEnvironment  # pants: no-infer-dep
from temporalio.worker import Worker  # pants: no-infer-dep

import workflows.journey_workflow as workflows_module
from workflows.journey_workflow import JourneyWorkflow
from apis.travelagent.v1.journey import Journey, Route


def test_print_journey_workflow_logs_supported_and_unknown_routes(monkeypatch) -> None:
    info_messages = []
    warning_messages = []

    def fake_info(message: str) -> None:
        info_messages.append(message)

    def fake_warning(message: str) -> None:
        warning_messages.append(message)

    monkeypatch.setattr(workflows_module.workflow.logger, "info", fake_info)
    monkeypatch.setattr(workflows_module.workflow.logger, "warning", fake_warning)

    class FakeNexusClient:
        async def execute_operation(self, *_args, **_kwargs):
            return None

    monkeypatch.setattr(
        workflows_module.workflow,
        "create_nexus_client",
        lambda **_kwargs: FakeNexusClient(),
    )

    journey = Journey(
        id="test-journey-1",
        creation_date="2024-03-19T10:00:00Z",
        routes=[
            Route(
                schema_version="airliner/v1",
                properties={
                    "id": "flight-101",
                    "aircraft_id": "A380-123",
                    "creation_date": "2024-03-19T10:00:00Z",
                    "departure": "CDGA",
                    "destination": "ORLY",
                    "estimated_takeoff": "2024-03-19T10:30:00Z",
                    "estimated_landing": "2024-03-19T11:30:00Z",
                },
            ),
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
            ),
            Route(
                schema_version="tourguide/v1",
                properties={"city": "Rome"},
            ),
            Route(
                schema_version="bikerental/v1",
                properties={
                    "id": "bp-20260313-001",
                    "bike_id": "BIKE-E200-07",
                    "pickup_location": {
                        "street": "Central Park West",
                        "house_number": "10",
                        "city": "New York",
                        "postal_code": "10024",
                        "country_code": "US",
                    },
                    "dropoff_location": {
                        "street": "Broadway",
                        "house_number": "200",
                        "city": "New York",
                        "postal_code": "10023",
                        "country_code": "US",
                    },
                    "estimated_pickup": "2026-03-13T18:00:00Z",
                    "estimated_dropoff": "2026-03-13T19:30:00Z",
                },
            ),
        ],
    )

    asyncio.run(JourneyWorkflow().run(journey))

    assert "Processing airliner route to ORLY" in info_messages
    assert "Processing city taxi route to Rome" in info_messages
    assert "Processing bike rental route to New York" in info_messages
    assert warning_messages[0] == "Unknown route type tourguide/v1"


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
                    workflows=[JourneyWorkflow],
                    activity_executor=activity_executor,
                ):
                    return await env.client.execute_workflow(
                        JourneyWorkflow.run,
                        journey,
                        id=workflow_id,
                        task_queue=task_queue,
                    )

    asyncio.run(run_workflow())
