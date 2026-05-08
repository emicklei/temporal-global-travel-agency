from datetime import timedelta
from temporalio import workflow

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService

from apis.bikerental.v1.bike_plan import BikePlan
from apis.bikerental.v1.service import BikeNexusService

from apis.citytaxi.v1.taxi_plan import TaxiPlan
from apis.citytaxi.v1.service import TaxiNexusService 

from apis.tourguide.v1.tour_plan import TourPlan
from apis.tourguide.v1.service import TourNexusService

from apis.travelagent.v1.journey import Journey
from apis.travelagent.v1.journey import Route 

# App names
APP_AIRLINER = "airliner"
APP_CITYTAXI = "citytaxi"
APP_BIKERENTAL = "bikerental"
APP_TOURGUIDE = "tourguide"

# Nexus endpoints
NEXUS_AIRLINER = "nexus-airliner-endpoint"
NEXUS_CITYTAXI = "nexus-citytaxi-endpoint"
NEXUS_BIKERENTAL = "nexus-bikerental-endpoint"
NEXUS_TOURGUIDE = "nexus-tourguide-endpoint"
NexusTimeout = timedelta(hours=1)


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
            if app == APP_AIRLINER:
                plan = FlightPlan(**route_properties)
                FlightPlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            elif app == APP_CITYTAXI:
                plan = TaxiPlan(**route_properties)
                TaxiPlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            elif app == APP_BIKERENTAL:
                plan = BikePlan(**route_properties)
                BikePlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))
            elif app == APP_TOURGUIDE:
                plan = TourPlan(**route_properties)
                TourPlan.model_validate(plan)
                app_routes.append(ApplicationRoute(app, route, plan))                
            else:
                workflow.logger.warning(f"Unknown route type {route.schema_version}")

        for app_route in app_routes:
            # set the parent_id of the plan to the journey id so that it can be used for correlation in the downstream workflows and activities.
            app_route.plan.parent_id = journey.id

            # use the schema_version to determine which workflow to start
            if app_route.app == APP_AIRLINER:
                workflow.logger.info(
                    f"Processing airliner route to {app_route.plan.destination}"
                )
                nexus_client = workflow.create_nexus_client(
                    service=FlightNexusService,
                    endpoint=NEXUS_AIRLINER,
                )
                await nexus_client.execute_operation(
                    FlightNexusService.execute_plan,
                    app_route.plan,
                    schedule_to_close_timeout=NexusTimeout,
                )

            elif app_route.app == APP_CITYTAXI:
                workflow.logger.info(
                    f"Processing city taxi route to {app_route.plan.dropoff_address.city}"
                )
                nexus_client = workflow.create_nexus_client(
                    service=TaxiNexusService,
                    endpoint=NEXUS_CITYTAXI,
                )
                await nexus_client.execute_operation(
                    TaxiNexusService.execute_plan,
                    app_route.plan, 
                    schedule_to_close_timeout=NexusTimeout,
                )
            elif app_route.app == APP_BIKERENTAL:
                workflow.logger.info(
                    f"Processing bike rental route to {app_route.plan.dropoff_location.city}"
                )
                nexus_client = workflow.create_nexus_client(
                    service=BikeNexusService,
                    endpoint=NEXUS_BIKERENTAL,
                )
                await nexus_client.execute_operation(
                    BikeNexusService.execute_plan,
                    app_route.plan, 
                    schedule_to_close_timeout=NexusTimeout,
                )
            elif app_route.app == APP_TOURGUIDE:
                workflow.logger.info(
                    f"Processing tour guide route for city {app_route.plan.location.city}"
                )
                nexus_client = workflow.create_nexus_client(
                    service=TourNexusService,
                    endpoint=NEXUS_TOURGUIDE,
                )
                await nexus_client.execute_operation(
                    TourNexusService.execute_plan,
                    app_route.plan, 
                    schedule_to_close_timeout=NexusTimeout,
                )
            else:
                workflow.logger.warning(
                    f"Unknown route type {app_route.route.schema_version}"
                )
