import argparse
import sys
import types

import pytest
import travelagent.main as main_module
import travelagent.starter as starter_module
import travelagent.worker as worker_module
from travelagent.activities import compose_hello_message
from travelagent.main import run_from_args
from travelagent.starter import build_workflow_id


@pytest.mark.asyncio
async def test_run_from_args_worker_mode(monkeypatch) -> None:
    called = {}

    async def fake_run_worker(hostport: str, namespace: str, task_queue: str) -> None:
        called["values"] = (hostport, namespace, task_queue)

    monkeypatch.setattr(main_module, "run_worker", fake_run_worker)

    args = argparse.Namespace(
        mode="worker",
        hostport="localhost:7233",
        namespace="default",
        task_queue="travelagent-hello-task-queue",
    )
    await run_from_args(args)

    assert called["values"] == (
        "localhost:7233",
        "default",
        "travelagent-hello-task-queue",
    )


@pytest.mark.asyncio
async def test_run_from_args_start_mode(capsys, monkeypatch) -> None:
    async def fake_run_starter(name: str, hostport: str, namespace: str, task_queue: str) -> str:
        assert name == "Ada"
        return "Hello, Ada! Welcome to Temporal Travel Agent."

    monkeypatch.setattr(main_module, "run_starter", fake_run_starter)

    args = argparse.Namespace(
        mode="start",
        name="Ada",
        hostport="localhost:7233",
        namespace="default",
        task_queue="travelagent-hello-task-queue",
    )
    await run_from_args(args)

    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, Ada! Welcome to Temporal Travel Agent."


def test_compose_hello_message() -> None:
    assert compose_hello_message("Ada") == "Hello, Ada! Welcome to Temporal Travel Agent."


def test_build_workflow_id_normalizes_name() -> None:
    assert build_workflow_id("  Ada  Lovelace ") == "travelagent-hello-ada-lovelace"


def test_build_workflow_id_falls_back_for_blank_name() -> None:
    assert build_workflow_id("   ") == "travelagent-hello-guest"


@pytest.mark.asyncio
async def test_run_worker_wires_temporal_components(monkeypatch) -> None:
    worker_init = {}

    class DummyClient:
        pass

    class DummyWorker:
        def __init__(self, client, task_queue, workflows, activities):
            worker_init["values"] = (client, task_queue, workflows, activities)

        async def run(self) -> None:
            return None

    class DummyClientAPI:
        @staticmethod
        async def connect(hostport: str, namespace: str):
            assert hostport == "localhost:7233"
            assert namespace == "default"
            return DummyClient()

    temporalio_module = types.ModuleType("temporalio")
    client_module = types.ModuleType("temporalio.client")
    worker_api_module = types.ModuleType("temporalio.worker")
    client_module.Client = DummyClientAPI
    worker_api_module.Worker = DummyWorker

    monkeypatch.setitem(sys.modules, "temporalio", temporalio_module)
    monkeypatch.setitem(sys.modules, "temporalio.client", client_module)
    monkeypatch.setitem(sys.modules, "temporalio.worker", worker_api_module)

    await worker_module.run_worker()

    client, task_queue, workflows, activities = worker_init["values"]
    assert isinstance(client, DummyClient)
    assert task_queue == "travelagent-hello-task-queue"
    assert len(workflows) == 1
    assert len(activities) == 1


@pytest.mark.asyncio
async def test_run_starter_executes_workflow(monkeypatch) -> None:
    class DummyClient:
        async def execute_workflow(self, run_method, name, id, task_queue):
            assert name == "Ada"
            assert id == "travelagent-hello-ada"
            assert task_queue == "travelagent-hello-task-queue"
            assert run_method is not None
            return "hello-result"

    class DummyClientAPI:
        @staticmethod
        async def connect(hostport: str, namespace: str):
            assert hostport == "localhost:7233"
            assert namespace == "default"
            return DummyClient()

    temporalio_module = types.ModuleType("temporalio")
    client_module = types.ModuleType("temporalio.client")
    client_module.Client = DummyClientAPI

    monkeypatch.setitem(sys.modules, "temporalio", temporalio_module)
    monkeypatch.setitem(sys.modules, "temporalio.client", client_module)

    result = await starter_module.run_starter("Ada")
    assert result == "hello-result"
