import json
from pathlib import Path
import asyncio
import os
import uuid

from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter


from apis.airliner.v1.flight_plan import FlightPlan
from workflows.caller_workflow import CallerWorkflow

CALLER_TASK_QUEUE = "travelagent-task-queue"
NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "travelagent")
TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")

def _load_fixture1() -> FlightPlan:
  fixture_path = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "plan1.json"
  payload = json.loads(fixture_path.read_text(encoding="utf-8"))

  for route in payload.get("routes", []):
      if route.get("schema_version") == "airliner/v1":
          return FlightPlan.model_validate(route.get("properties", {}))

  raise ValueError("No airliner/v1 route found in tests/fixtures/plan1.json")

async def main():
  client = await Client.connect(TEMPORAL_ADDRESS,
    namespace=NAMESPACE, 
    data_converter=pydantic_data_converter)

  async with Worker(
      client,
      task_queue=CALLER_TASK_QUEUE,
      workflows=[CallerWorkflow],
  ):
      plan = _load_fixture1()
      print("client execute CallerWorkflow.run", plan)

      result = await client.execute_workflow(
          CallerWorkflow.run,
          plan,
          id=f"caller-workflow-{uuid.uuid4()}",
          task_queue=CALLER_TASK_QUEUE,
      )
      print("Workflow result:", result)


if __name__ == "__main__":
  asyncio.run(main())


