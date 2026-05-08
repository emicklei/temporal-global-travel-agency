from datetime import timedelta
from temporalio import workflow

from apis.airliner.v1.flight_plan import FlightPlan
from logger.activities import log_as_json


@workflow.defn
class RunFlightPlanWorkflow:
    @workflow.run
    async def run(self, flight_plan: FlightPlan) -> None:
        workflow.logger.info(f"RunFlightPlanWorkflow started with flight plan: {flight_plan.id} journey={flight_plan.parent_id}")

        await workflow.execute_activity(
            log_as_json,
            args=["Flight plan", flight_plan.model_dump()],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
