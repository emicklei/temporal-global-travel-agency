import nexusrpc

from apis.tourguide.v1.tour_plan import TourPlan


@nexusrpc.service
class TourNexusService:
    execute_plan: nexusrpc.Operation[TourPlan, str]
