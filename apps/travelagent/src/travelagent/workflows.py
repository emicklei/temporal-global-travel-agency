from temporalio import workflow

from generated.travelagent.v1.journey import Journey


@workflow.defn
class PrintJourneyWorkflow:
    @workflow.run
    async def run(self, journey: Journey) -> None:
        print(journey.model_dump_json(indent=2))

        for route in journey.routes:
            print(route.model_dump_json(indent=2))
