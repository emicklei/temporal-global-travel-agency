from datetime import timedelta
import inspect
from typing import Any

try:
    from temporalio import workflow  # pants: no-infer-dep
except ModuleNotFoundError:
    class _WorkflowShim:
        @staticmethod
        def defn(target):
            return target

        @staticmethod
        def run(fn):
            return fn

        @staticmethod
        async def execute_activity(
            activity_fn, *args: Any, **_kwargs: Any
        ) -> Any:
            result = activity_fn(*args)
            if inspect.isawaitable(result):
                return await result
            return result

    workflow = _WorkflowShim()

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
