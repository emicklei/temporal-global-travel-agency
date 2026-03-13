from datetime import timedelta
from temporalio import workflow

from .activities import compose_hello_message


@workflow.defn
class HelloTravelWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            compose_hello_message,
            name,
            schedule_to_close_timeout=timedelta(seconds=10),
        )
