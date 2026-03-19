from temporalio.client import Client
from temporalio.worker import Worker

from .workflows import PrintJourneyWorkflow

DEFAULT_TASK_QUEUE = "travelagent-print-journey-task-queue"


async def run_worker(
    hostport: str = "localhost:7233",
    namespace: str = "default",
    task_queue: str = DEFAULT_TASK_QUEUE,
) -> None:
    client = await Client.connect(hostport, namespace=namespace)
    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[PrintJourneyWorkflow],
        activities=[],
    )
    await worker.run()
