import asyncio

import travelagent.worker as worker_module


def test_run_worker_creates_and_runs_worker(monkeypatch) -> None:
    captured = {}

    class DummyClient:
        pass

    class DummyWorker:
        def __init__(self, client, task_queue, workflows, activities):
            captured["init"] = (client, task_queue, workflows, activities)

        async def run(self) -> None:
            captured["ran"] = True

    async def fake_connect(hostport: str, namespace: str):
        assert hostport == "localhost:7233"
        assert namespace == "default"
        return DummyClient()

    monkeypatch.setattr(worker_module.Client, "connect", fake_connect)
    monkeypatch.setattr(worker_module, "Worker", DummyWorker)

    asyncio.run(worker_module.run_worker())

    client, task_queue, workflows, activities = captured["init"]
    assert isinstance(client, DummyClient)
    assert task_queue == "travelagent-hello-task-queue"
    assert workflows == [worker_module.HelloTravelWorkflow]
    assert activities == [worker_module.compose_hello_message]
    assert captured["ran"] is True
