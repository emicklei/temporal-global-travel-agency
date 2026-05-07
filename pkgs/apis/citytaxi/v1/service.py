import nexusrpc

from apis.citytaxi.v1.taxi_plan import TaxiPlan


@nexusrpc.service
class TaxiNexusService:
    execute_plan: nexusrpc.Operation[TaxiPlan, str]
