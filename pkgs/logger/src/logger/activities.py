import asyncio
import json
import logging
import random
from typing import Any

from temporalio import activity  # pants: no-infer-dep


@activity.defn
async def log_as_json(message: str, data: dict[str, Any]) -> None:
    """
    Write a message and associated data as a JSON log entry.

    Args:
        message: The log message to write
        data: A dictionary to be serialized as JSON
    """ 

    # Simulate some delay to demonstrate Temporal's activity heartbeat and timeout features.
    # random between 5 and 10 seconds, which is longer than the typical heartbeat timeout used in Temporal activities.
    delay = 5 + 5 * random.random()
    activity.logger.info(f"Simulating traveling, sleep for {delay} seconds")
    await asyncio.sleep(delay)

    activity.logger.info(f"{message}: {json.dumps(data, indent=2)}")
