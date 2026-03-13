import argparse
import sys
import types

import pytest  # pants: no-infer-dep
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


@pytest.mark.asyncio
async def test_run_worker_uses_custom_arguments(monkeypatch) -> None:
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
            assert hostport == "temporal.example:7233"
            assert namespace == "travel"
            return DummyClient()

    temporalio_module = types.ModuleType("temporalio")
    client_module = types.ModuleType("temporalio.client")
    worker_api_module = types.ModuleType("temporalio.worker")
    client_module.Client = DummyClientAPI
    worker_api_module.Worker = DummyWorker

    monkeypatch.setitem(sys.modules, "temporalio", temporalio_module)
    monkeypatch.setitem(sys.modules, "temporalio.client", client_module)
    monkeypatch.setitem(sys.modules, "temporalio.worker", worker_api_module)

    await worker_module.run_worker(
        hostport="temporal.example:7233",
        namespace="travel",
        task_queue="custom-queue",
    )

    _, task_queue, _, _ = worker_init["values"]
    assert task_queue == "custom-queue"


@pytest.mark.asyncio
async def test_run_starter_uses_custom_arguments(monkeypatch) -> None:
    class DummyClient:
        async def execute_workflow(self, run_method, name, id, task_queue):
            assert name == "Grace"
            assert id == "travelagent-hello-grace"
            assert task_queue == "custom-queue"
            assert run_method is not None
            return "hello-result"

    class DummyClientAPI:
        @staticmethod
        async def connect(hostport: str, namespace: str):
            assert hostport == "temporal.example:7233"
            assert namespace == "travel"
            return DummyClient()

    temporalio_module = types.ModuleType("temporalio")
    client_module = types.ModuleType("temporalio.client")
    client_module.Client = DummyClientAPI

    monkeypatch.setitem(sys.modules, "temporalio", temporalio_module)
    monkeypatch.setitem(sys.modules, "temporalio.client", client_module)

    result = await starter_module.run_starter(
        "Grace",
        hostport="temporal.example:7233",
        namespace="travel",
        task_queue="custom-queue",
    )
    assert result == "hello-result"


def test_parse_args_worker_custom(monkeypatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "travelagent.main",
            "worker",
            "--hostport",
            "temporal.example:7233",
            "--namespace",
            "travel",
            "--task-queue",
            "custom-queue",
        ],
    )

    args = main_module.parse_args()
    assert args.mode == "worker"
    assert args.hostport == "temporal.example:7233"
    assert args.namespace == "travel"
    assert args.task_queue == "custom-queue"


def test_parse_args_start_defaults(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["travelagent.main", "start"])

    args = main_module.parse_args()
    assert args.mode == "start"
    assert args.name == "Temporal traveler"
    assert args.hostport == "localhost:7233"
    assert args.namespace == "default"
    assert args.task_queue == "travelagent-hello-task-queue"


def test_main_invokes_asyncio_run(monkeypatch) -> None:
    called = {}
    original_asyncio_run = main_module.asyncio.run

    def fake_parse_args() -> argparse.Namespace:
        return argparse.Namespace(
            mode="start",
            name="Ada",
            hostport="localhost:7233",
            namespace="default",
            task_queue="travelagent-hello-task-queue",
        )

    async def fake_run_from_args(args: argparse.Namespace) -> None:
        called["args"] = args

    def fake_asyncio_run(coroutine) -> None:
        original_asyncio_run(coroutine)

    monkeypatch.setattr(main_module, "parse_args", fake_parse_args)
    monkeypatch.setattr(main_module, "run_from_args", fake_run_from_args)
    monkeypatch.setattr(main_module.asyncio, "run", fake_asyncio_run)

    main_module.main()
    assert called["args"].mode == "start"
