import json
import logging
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
    logger = logging.getLogger(__name__)
    logger.info(f"{message}: {json.dumps(data, indent=2)}")
