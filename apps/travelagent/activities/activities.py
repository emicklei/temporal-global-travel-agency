from datetime import timedelta
from temporalio import activity
from temporalio import workflow

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService

NEXUS_ENDPOINT = "nexus-airliner-endpoint"

@activity.defn
async def call_airliner_nexus_service(plan : FlightPlan) -> str:
        nexus_client = workflow.create_nexus_client(
            service=FlightNexusService,
            endpoint=NEXUS_ENDPOINT,
        )

        return await nexus_client.execute_operation(
            FlightNexusService.execute_plan,
            plan,
            schedule_to_close_timeout=timedelta(seconds=10),
        )