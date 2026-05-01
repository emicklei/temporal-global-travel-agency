from datetime import timedelta
from temporalio import workflow

from apis.airliner.v1.flight_plan import FlightPlan
from logger.activities import log_as_json


@workflow.defn
class RunFlightPlanWorkflow:
    @workflow.run
    async def run(self, flight_plan: FlightPlan) -> None:
        await workflow.execute_activity(
            log_as_json,
            "Flight plan",
            flight_plan.model_dump(),
            schedule_to_close_timeout=timedelta(seconds=10),
        )
