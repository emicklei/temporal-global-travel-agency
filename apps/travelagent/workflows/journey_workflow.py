from datetime import timedelta
from temporalio import workflow

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService
from apis.bikerental.v1.bike_plan import BikePlan
from apis.citytaxi.v1.taxi_plan import TaxiPlan
from apis.travelagent.v1.journey import Journey
from apis.travelagent.v1.journey import Route
from workflows.caller_workflow import NEXUS_ENDPOINT


class ApplicationRoute:
    def __init__(self, app: str, route: Route, plan: any):
        self.route = route
        self.app = app
        self.plan = plan


@workflow.defn
class JourneyWorkflow:
    @workflow.run
    async def run(self, journey: Journey) -> None:
        Journey.model_validate(journey)
        # validate all the routes in the journey first before processing any of them.
        # collect the plans
        app_routes = []
        for route in journey.routes:
            route_properties = (
                route.properties.model_dump()
                if hasattr(route.properties, "model_dump")
                else route.properties
            )
            # use the schema_version to determine which workflow to start
            app = route.schema_version.split("/")[0]
            if app == "airliner":
                plan = FlightPlan(**route_properties)
                FlightPlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            elif app == "citytaxi":
                plan = TaxiPlan(**route_properties)
                TaxiPlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            elif app == "bikerental":
                plan = BikePlan(**route_properties)
                BikePlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            else:
                workflow.logger.warning(f"Unknown route type {route.schema_version}")

        for app_route in app_routes:
            # use the schema_version to determine which workflow to start
            if app_route.app == "airliner":
                workflow.logger.info(
                    f"Processing airliner route to {app_route.plan.destination}"
                )
                nexus_client = workflow.create_nexus_client(
                    service=FlightNexusService,
                    endpoint=NEXUS_ENDPOINT,
                )
                await nexus_client.execute_operation(
                    FlightNexusService.execute_plan,
                    app_route.plan,
                    schedule_to_close_timeout=timedelta(seconds=10),
                )

            elif app_route.app == "citytaxi":
                workflow.logger.info(
                    f"Processing city taxi route to {app_route.plan.dropoff_address.city}"
                )
            elif app_route.app == "bikerental":
                workflow.logger.info(
                    f"Processing bike rental route to {app_route.plan.dropoff_location.city}"
                )
            else:
                workflow.logger.warning(
                    f"Unknown route type {app_route.route.schema_version}"
                )
