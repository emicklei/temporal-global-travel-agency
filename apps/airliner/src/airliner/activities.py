from typing import Any

import structlog
from temporalio import activity


logger = structlog.get_logger(__name__)


@activity.defn
async def log_as_json(message: str, data: dict[str, Any]) -> None:
    logger.info("flight_plan", message=message, data=data)


__all__ = ["log_as_json"]
