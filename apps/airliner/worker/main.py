import asyncio
import os

from temporalio.contrib.pydantic import pydantic_data_converter
from temporalio.client import Client
from temporalio.worker import Worker

from workflows.workflows import RunFlightPlanWorkflow
from logger.activities import log_as_json
from .handler import FlightNexusServiceHandler


async def main():
  temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
  temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "airliner")

  client = await Client.connect(
      temporal_address,
      namespace=temporal_namespace,
      data_converter=pydantic_data_converter,
  )
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