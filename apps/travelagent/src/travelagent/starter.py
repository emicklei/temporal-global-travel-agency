from temporalio.client import Client

from .worker import DEFAULT_TASK_QUEUE
from .workflows import HelloTravelWorkflow


def build_workflow_id(name: str) -> str:
    normalized_name = "-".join(part for part in name.strip().lower().split() if part)
    if not normalized_name:
        normalized_name = "guest"
    return f"travelagent-hello-{normalized_name}"


async def run_starter(
    name: str,
    hostport: str = "localhost:7233",
    namespace: str = "default",
    task_queue: str = DEFAULT_TASK_QUEUE,
) -> str:
    client = await Client.connect(hostport, namespace=namespace)
    return await client.execute_workflow(
        HelloTravelWorkflow.run,
        name,
        id=build_workflow_id(name),
        task_queue=task_queue,
    )
