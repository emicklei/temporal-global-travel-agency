import uuid
import logging

import nexusrpc.handler
from temporalio import nexus

from apis.tourguide.v1.tour_plan import TourPlan
from apis.tourguide.v1.service import TourNexusService

from workflows.workflows import RunTourPlanWorkflow


logger = logging.getLogger(__name__)


@nexusrpc.handler.service_handler(service=TourNexusService)
class TourNexusServiceHandler:
    @nexus.workflow_run_operation
    async def execute_plan(
        self, ctx: nexus.WorkflowRunOperationContext, input: TourPlan
    ) -> nexus.WorkflowHandle[str]:
        logger.debug("Received tour plan: %s", input)

        return await ctx.start_workflow(
            RunTourPlanWorkflow.run,
            input,
            id=f"tourplan-{uuid.uuid4()}",
        )
