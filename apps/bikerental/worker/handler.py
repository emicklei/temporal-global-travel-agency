import uuid
import logging

import nexusrpc.handler
from temporalio import nexus

from apis.bikerental.v1.bike_plan import BikePlan
from apis.bikerental.v1.service import BikeNexusService

from workflows.workflows import RunBikePlanWorkflow


logger = logging.getLogger(__name__)


@nexusrpc.handler.service_handler(service=BikeNexusService)
class BikeNexusServiceHandler:
    @nexus.workflow_run_operation
    async def execute_plan(
        self, ctx: nexus.WorkflowRunOperationContext, input: BikePlan
    ) -> nexus.WorkflowHandle[str]:
        logger.debug("Received bike plan: %s", input)

        return await ctx.start_workflow(
            RunBikePlanWorkflow.run,
            input,
            id=f"bikeplan-{uuid.uuid4()}",
        )
