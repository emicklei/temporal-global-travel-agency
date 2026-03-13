import asyncio

import travelagent.starter as starter_module


def test_run_starter_executes_workflow_call(monkeypatch) -> None:
    class DummyClient:
        async def execute_workflow(self, run_method, name, id, task_queue):
            assert run_method is starter_module.HelloTravelWorkflow.run
            assert name == "Ada"
            assert id == "travelagent-hello-ada"
            assert task_queue == "travelagent-hello-task-queue"
            return "workflow-result"

    async def fake_connect(hostport: str, namespace: str):
        assert hostport == "localhost:7233"
        assert namespace == "default"
        return DummyClient()

    monkeypatch.setattr(starter_module.Client, "connect", fake_connect)

    result = asyncio.run(starter_module.run_starter("Ada"))
    assert result == "workflow-result"
