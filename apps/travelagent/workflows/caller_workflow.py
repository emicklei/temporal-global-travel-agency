from datetime import timedelta
from temporalio import workflow

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService
from activities.activities import call_airliner_nexus_service

NEXUS_ENDPOINT = "nexus-airliner-endpoint"


@workflow.defn
class CallerWorkflow:
    @workflow.run
    async def run(self, plan: FlightPlan) -> str:
        workflow.logger.info(f"CallerWorkflow started with plan={plan.id} journey={plan.parent_id}")

        nexus_client = workflow.create_nexus_client(
            service=FlightNexusService,
            endpoint=NEXUS_ENDPOINT,
        )

        return await nexus_client.execute_operation(
            FlightNexusService.execute_plan,
            plan,
            schedule_to_close_timeout=timedelta(seconds=10),
        )

        # return await workflow.execute_activity(
        #     call_airliner_nexus_service,
        #     plan,
        #     start_to_close_timeout=timedelta(seconds=10),
        # )
