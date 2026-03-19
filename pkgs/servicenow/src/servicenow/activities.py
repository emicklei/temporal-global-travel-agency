from __future__ import annotations

from typing import Any

from temporalio import activity  # pants: no-infer-dep

from .client import ServiceNowClient


@activity.defn
def create_cmdb_change_activity(
    instance_url: str,
    username: str,
    password: str,
    change: dict[str, Any],
) -> dict[str, Any]:
    """Create a CMDB change request in ServiceNow."""
    client = ServiceNowClient(
        instance_url=instance_url,
        username=username,
        password=password,
    )
    return client.create_change(change)
