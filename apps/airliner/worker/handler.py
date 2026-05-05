import uuid
import logging

import nexusrpc.handler
from temporalio import nexus

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService

from workflows.workflows import RunFlightPlanWorkflow


logger = logging.getLogger(__name__)


@nexusrpc.handler.service_handler(service=FlightNexusService)
class FlightNexusServiceHandler:
  @nexus.workflow_run_operation
  async def execute_plan(
      self, ctx: nexus.WorkflowRunOperationContext, input: FlightPlan
  ) -> nexus.WorkflowHandle[str]:

      logger.debug("Received flight plan: %s", input)

      return await ctx.start_workflow(
          RunFlightPlanWorkflow.run,
          input,
          id=f"flightplan-{uuid.uuid4()}",

          # Task queue defaults to the task queue this Operation is handled on.
      )