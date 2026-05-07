import uuid
import logging

logger = logging.getLogger(__name__)

import nexusrpc.handler
from temporalio import nexus

from apis.airliner.v1.flight_plan import FlightPlan
from apis.airliner.v1.service import FlightNexusService

from workflows.workflows import RunFlightPlanWorkflow


@nexusrpc.handler.service_handler(service=FlightNexusService)
class FlightNexusServiceHandler:
    @nexus.workflow_run_operation
    async def execute_plan(
        self, ctx: nexus.WorkflowRunOperationContext, plan: FlightPlan
    ) -> nexus.WorkflowHandle[str]:
        # not in a workflow context, so use standard logging
        logger.info(f"Nexus handler received flight plan={plan.id}, journey={plan.parentId}")

        return await ctx.start_workflow(
            RunFlightPlanWorkflow.run,
            plan,
            id=f"{plan.id}-workflow-{uuid.uuid4()}",
            # Task queue defaults to the task queue this Operation is handled on.
        )
