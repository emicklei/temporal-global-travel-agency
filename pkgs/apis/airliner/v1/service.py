import nexusrpc

from apis.airliner.v1.flight_plan import FlightPlan

@nexusrpc.service
class FlightNexusService:
  execute_plan: nexusrpc.Operation[FlightPlan, str]