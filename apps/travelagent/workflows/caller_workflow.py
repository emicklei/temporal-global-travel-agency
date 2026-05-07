from datetime import timedelta
from temporalio import workflow

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService

NEXUS_ENDPOINT = "nexus-airliner-endpoint"


@workflow.defn
class CallerWorkflow:
    @workflow.run
    async def run(self, plan: FlightPlan) -> str:
        workflow.logger.info(f"CallerWorkflow started with plan: {plan.id}")

        nexus_client = workflow.create_nexus_client(
            service=FlightNexusService,
            endpoint=NEXUS_ENDPOINT,
        )

        return await nexus_client.execute_operation(
            FlightNexusService.execute_plan,
            plan,
            schedule_to_close_timeout=timedelta(seconds=10),
        )
