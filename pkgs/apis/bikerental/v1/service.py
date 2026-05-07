import nexusrpc

from apis.bikerental.v1.bike_plan import BikePlan


@nexusrpc.service
class BikeNexusService:
    execute_plan: nexusrpc.Operation[BikePlan, str]
