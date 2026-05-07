from datetime import timedelta
from temporalio import workflow

from apis.tourguide.v1.tour_plan import TourPlan
from logger.activities import log_as_json


@workflow.defn
class RunTourPlanWorkflow:
    @workflow.run
    async def run(self, tour_plan: TourPlan) -> None:
        await workflow.execute_activity(
            log_as_json,
            args=["Tour plan", tour_plan.model_dump()],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
