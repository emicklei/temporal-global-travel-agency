import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from workflows.journey_workflow import JourneyWorkflow
from logger.activities import log_as_json


async def main():
  client = await Client.connect("localhost:7233")
  worker = Worker(
      client,
      task_queue="travelagent-task-queue",
      workflows=[JourneyWorkflow],
      activities=[log_as_json]
  )
  print("TravelAgent worker started.")
  await worker.run()


if __name__ == "__main__":
  asyncio.run(main())