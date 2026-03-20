from temporalio import workflow

from generated.airliner.v1.flight_plan import FlightPlan
from generated.citytaxi.v1.taxi_plan import TaxiPlan
from generated.travelagent.v1.journey import Journey


@workflow.defn
class JourneyWorkflow:
    @workflow.run
    async def run(self, journey: Journey) -> None:
        workflow.logger.info(journey.model_dump_json(indent=2))

        for route in journey.routes:
            # use the schema_version to determine which workflow to start
            switch = route.schema_version.split("/")[0]
            if switch == "airliner":
                plan = FlightPlan(**route.properties)
                FlightPlan.validate(plan)
                workflow.logger.info(f"Processing airliner route to {plan.destination}")
            elif switch == "citytaxi":
                plan = TaxiPlan(**route.properties)
                TaxiPlan.validate(plan)
                workflow.logger.info(
                    f"Processing city taxi route to {plan.dropoff_address.city}"
                )
            else:
                workflow.logger.warning(f"Unknown route type {route.schema_version}")
