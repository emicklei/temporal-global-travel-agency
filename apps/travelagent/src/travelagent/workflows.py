from temporalio import workflow

from generated.airliner.v1.flight_plan import FlightPlan
from generated.citytaxi.v1.taxi_plan import TaxiPlan
from generated.travelagent.v1.journey import Journey
from generated.travelagent.v1.journey import Route


class ApplicationRoute:
    def __init__(self, app: str, route: Route, plan: any):
        self.route = route
        self.app = app
        self.plan = plan


@workflow.defn
class JourneyWorkflow:
    @workflow.run
    async def run(self, journey: Journey) -> None:
        Journey.validate(journey)
        # validate all the routes in the journey first before processing any of them.
        # collect the plans
        app_routes = []
        for route in journey.routes:
            # use the schema_version to determine which workflow to start
            app = route.schema_version.split("/")[0]
            if app == "airliner":
                plan = FlightPlan(**route.properties)
                FlightPlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            elif app == "citytaxi":
                plan = TaxiPlan(**route.properties)
                TaxiPlan.validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            else:
                workflow.logger.warning(f"Unknown route type {route.schema_version}")

        for app_route in app_routes:
            # use the schema_version to determine which workflow to start
            if app_route.app == "airliner":
                workflow.logger.info(
                    f"Processing airliner route to {app_route.plan.destination}"
                )
            elif app_route.app == "citytaxi":
                workflow.logger.info(
                    f"Processing city taxi route to {app_route.plan.dropoff_address.city}"
                )
            else:
                workflow.logger.warning(
                    f"Unknown route type {app_route.route.schema_version}"
                )
