from datetime import timedelta
from temporalio import workflow

from generated.travelagent.v1.journey import Journey

from .activities import compose_hello_message


@workflow.defn
class HelloTravelWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            compose_hello_message,
            name,
            schedule_to_close_timeout=timedelta(seconds=10),
        )


@workflow.defn
class PrintJourneyWorkflow:
    @workflow.run
    async def run(self, journey: Journey) -> None:
        print(journey.model_dump_json(indent=2))
