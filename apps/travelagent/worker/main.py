import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter

from workflows.journey_workflow import JourneyWorkflow
from workflows.caller_workflow import CallerWorkflow

DEFAULT_TASK_QUEUE = "travelagent-task-queue"


async def run_worker(
    hostport: str = "localhost:7233",
    namespace: str = "travelagent",
    task_queue: str = DEFAULT_TASK_QUEUE,
) -> None:
    client = await Client.connect(hostport, namespace=namespace, data_converter=pydantic_data_converter)
    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[JourneyWorkflow, CallerWorkflow],
        activities=[],
    )
    print("TravelAgent worker started.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(run_worker())
