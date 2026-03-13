from datetime import timedelta
from uuid import uuid4

import pytest  # pants: no-infer-dep
from temporalio.testing import WorkflowEnvironment  # pants: no-infer-dep
from temporalio.worker import Worker  # pants: no-infer-dep

import travelagent.workflows as workflows_module
from travelagent.activities import compose_hello_message
from travelagent.workflows import HelloTravelWorkflow


@pytest.mark.asyncio
async def test_hello_travel_workflow_executes_activity_with_expected_arguments(monkeypatch) -> None:
    captured = {}

    async def fake_execute_activity(activity_fn, name, schedule_to_close_timeout):
        captured["activity_fn"] = activity_fn
        captured["name"] = name
        captured["timeout"] = schedule_to_close_timeout
        return "Hello, Ada! Welcome to Temporal Travel Agent."

    monkeypatch.setattr(workflows_module.workflow, "execute_activity", fake_execute_activity)

    result = await HelloTravelWorkflow().run("Ada")

    assert result == "Hello, Ada! Welcome to Temporal Travel Agent."
    assert captured["activity_fn"] is workflows_module.compose_hello_message
    assert captured["name"] == "Ada"
    assert captured["timeout"] == timedelta(seconds=10)


@pytest.mark.asyncio
async def test_hello_travel_workflow_runs_in_temporal_test_environment() -> None:
    async with await WorkflowEnvironment.start_time_skipping() as env:
        task_queue = f"travelagent-test-{uuid4()}"
        workflow_id = f"travelagent-hello-{uuid4()}"

        async with Worker(
            env.client,
            task_queue=task_queue,
            workflows=[HelloTravelWorkflow],
            activities=[compose_hello_message],
        ):
            result = await env.client.execute_workflow(
                HelloTravelWorkflow.run,
                "Ada",
                id=workflow_id,
                task_queue=task_queue,
            )

    assert result == "Hello, Ada! Welcome to Temporal Travel Agent."
