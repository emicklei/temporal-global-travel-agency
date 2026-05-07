import argparse
import asyncio
import json
from pathlib import Path
import os
import uuid
from apis.travelagent.v1.journey import Journey

from temporalio.client import ( Client )
from temporalio.common import ( SearchAttributeKey, SearchAttributePair, TypedSearchAttributes )
from temporalio.worker import Worker
from temporalio.contrib.pydantic import pydantic_data_converter
from workflows.journey_workflow import JourneyWorkflow

TASK_QUEUE = "travelagent-task-queue"
NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "travelagent")
TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")

journey_id_key = SearchAttributeKey.for_keyword("JourneyId")
DEFAULT_FIXTURE_PATH = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "plan1.json"


def _load_fixture(fixture_path: str | Path | None = None) -> Journey:
    fixture_path = Path(fixture_path) if fixture_path is not None else DEFAULT_FIXTURE_PATH
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    return Journey.model_validate(payload)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fixture-path",
        default=str(DEFAULT_FIXTURE_PATH),
        help="Path to the journey fixture JSON file.",
    )
    return parser.parse_args()


async def main(fixture_path: str | None = None):
    client = await Client.connect(
        TEMPORAL_ADDRESS, namespace=NAMESPACE, data_converter=pydantic_data_converter
    )

    async with Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[JourneyWorkflow],
    ):
        plan = _load_fixture(fixture_path)
        print("client execute JourneyWorkflow.run", plan.id)

        result = await client.execute_workflow(
            JourneyWorkflow.run,
            plan,
            id=f"{plan.id}-workflow-{uuid.uuid4()}",
            task_queue=TASK_QUEUE,
            search_attributes=TypedSearchAttributes(
                [SearchAttributePair(journey_id_key, plan.id)]
            ),
        )
        print("Workflow result:", result)


if __name__ == "__main__":
    args = _parse_args()
    asyncio.run(main(args.fixture_path))
