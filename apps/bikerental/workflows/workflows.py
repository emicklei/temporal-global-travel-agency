from datetime import timedelta
from temporalio import workflow

from apis.bikerental.v1.bike_plan import BikePlan
from logger.activities import log_as_json


@workflow.defn
class RunBikePlanWorkflow:
    @workflow.run
    async def run(self, bike_plan: BikePlan) -> None:
        workflow.logger.info(
            f"RunBikePlanWorkflow started with bike plan: {bike_plan.id} journey={bike_plan.parent_id}"
        )

        await workflow.execute_activity(
            log_as_json,
            args=["Bike plan", bike_plan.model_dump()],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
