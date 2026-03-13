from datetime import timedelta

import pytest  # pants: no-infer-dep

import travelagent.workflows as workflows_module
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
async def test_workflow_shim_execute_activity_supports_sync_functions() -> None:
    if not hasattr(workflows_module, "_WorkflowShim"):
        pytest.skip("Workflow shim is only available when temporalio is not installed")

    async def run_test() -> str:
        return await workflows_module._WorkflowShim.execute_activity(lambda name: f"Hi {name}", "Ada")

    result = await run_test()
    assert result == "Hi Ada"


@pytest.mark.asyncio
async def test_workflow_shim_execute_activity_supports_async_functions() -> None:
    if not hasattr(workflows_module, "_WorkflowShim"):
        pytest.skip("Workflow shim is only available when temporalio is not installed")

    async def async_activity(name: str) -> str:
        return f"Hi {name}"

    result = await workflows_module._WorkflowShim.execute_activity(async_activity, "Ada")
    assert result == "Hi Ada"
