from temporalio.client import Client
from temporalio.worker import Worker

from .activities import compose_hello_message
from .workflows import HelloTravelWorkflow

DEFAULT_TASK_QUEUE = "travelagent-hello-task-queue"


async def run_worker(
    hostport: str = "localhost:7233",
    namespace: str = "default",
    task_queue: str = DEFAULT_TASK_QUEUE,
) -> None:
    client = await Client.connect(hostport, namespace=namespace)
    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[HelloTravelWorkflow],
        activities=[compose_hello_message],
    )
    await worker.run()
