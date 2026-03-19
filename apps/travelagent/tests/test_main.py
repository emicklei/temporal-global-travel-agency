import argparse
import asyncio
import sys

import pytest  # pants: no-infer-dep
import travelagent.main as main_module
from travelagent.main import run_from_args


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
        task_queue="travelagent-print-journey-task-queue",
    )
    await run_from_args(args)

    assert called["values"] == (
        "localhost:7233",
        "default",
        "travelagent-print-journey-task-queue",
    )


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


def test_main_invokes_asyncio_run(monkeypatch) -> None:
    called = {}
    original_asyncio_run = main_module.asyncio.run

    def fake_parse_args() -> argparse.Namespace:
        return argparse.Namespace(
            mode="worker",
            hostport="localhost:7233",
            namespace="default",
            task_queue="travelagent-print-journey-task-queue",
        )

    async def fake_run_from_args(args: argparse.Namespace) -> None:
        called["args"] = args

    def fake_asyncio_run(coroutine) -> None:
        original_asyncio_run(coroutine)

    monkeypatch.setattr(main_module, "parse_args", fake_parse_args)
    monkeypatch.setattr(main_module, "run_from_args", fake_run_from_args)
    monkeypatch.setattr(main_module.asyncio, "run", fake_asyncio_run)

    main_module.main()
    assert called["args"].mode == "worker"


def test_run_from_args_worker_mode_via_asyncio_run(monkeypatch) -> None:
    called = {}

    async def fake_run_worker(hostport: str, namespace: str, task_queue: str) -> None:
        called["values"] = (hostport, namespace, task_queue)

    monkeypatch.setattr(main_module, "run_worker", fake_run_worker)

    args = argparse.Namespace(
        mode="worker",
        hostport="localhost:7233",
        namespace="default",
        task_queue="travelagent-print-journey-task-queue",
    )
    asyncio.run(main_module.run_from_args(args))

    assert called["values"] == (
        "localhost:7233",
        "default",
        "travelagent-print-journey-task-queue",
    )
