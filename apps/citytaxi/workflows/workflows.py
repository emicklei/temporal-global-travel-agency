from datetime import timedelta
from temporalio import workflow

from apis.citytaxi.v1.taxi_plan import TaxiPlan
from logger.activities import log_as_json


@workflow.defn
class RunTaxiPlanWorkflow:
    @workflow.run
    async def run(self, taxi_plan: TaxiPlan) -> None:
        await workflow.execute_activity(
            log_as_json,
            args=["Taxi plan", taxi_plan.model_dump()],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
