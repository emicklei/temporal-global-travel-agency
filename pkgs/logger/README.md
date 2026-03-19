# logger

A shared Temporal activity package for logging data as JSON.

## Usage

Import and use the `log_as_json` activity in your workflows:

```python
from logger.activities import log_as_json
from temporalio import workflow

@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self, data: dict) -> None:
        await workflow.execute_activity(
            log_as_json,
            "Processing data",
            data,
            schedule_to_close_timeout=timedelta(seconds=10),
        )
```

## Commands

From this directory:

```bash
make test
```
