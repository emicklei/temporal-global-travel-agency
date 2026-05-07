import uuid
import logging

import nexusrpc.handler
from temporalio import nexus

from apis.citytaxi.v1.taxi_plan import TaxiPlan
from apis.citytaxi.v1.service import TaxiNexusService

from workflows.workflows import RunTaxiPlanWorkflow


logger = logging.getLogger(__name__)


@nexusrpc.handler.service_handler(service=TaxiNexusService)
class TaxiNexusServiceHandler:
    @nexus.workflow_run_operation
    async def execute_plan(
        self, ctx: nexus.WorkflowRunOperationContext, input: TaxiPlan
    ) -> nexus.WorkflowHandle[str]:
        logger.debug("Received taxi plan: %s", input)

        return await ctx.start_workflow(
            RunTaxiPlanWorkflow.run,
            input,
            id=f"taxiplan-{uuid.uuid4()}",
        )
