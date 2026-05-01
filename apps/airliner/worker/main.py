import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows.workflows import RunFlightPlanWorkflow
from logger.activities import log_as_json
from .handler import FlightNexusServiceHandler


async def main():
  client = await Client.connect("localhost:7233")
  worker = Worker(
      client,
      task_queue="airliner-task-queue",
      workflows=[RunFlightPlanWorkflow],
      activities=[log_as_json],
      nexus_service_handlers=[FlightNexusServiceHandler()],
  )
  print("Airliner worker started.")
  await worker.run()


if __name__ == "__main__":
  asyncio.run(main())