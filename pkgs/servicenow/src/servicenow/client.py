from __future__ import annotations

import base64
import json
from typing import Any
from urllib import request


class ServiceNowClient:
    """Small client for creating change requests using ServiceNow Table API."""

    def __init__(
        self,
        instance_url: str,
        username: str,
        password: str,
        timeout_seconds: int = 10,
    ) -> None:
        self._instance_url = instance_url.rstrip("/")
        self._username = username
        self._password = password
        self._timeout_seconds = timeout_seconds

    def create_change(self, change: dict[str, Any]) -> dict[str, Any]:
        endpoint = f"{self._instance_url}/api/now/table/change_request"
        payload = json.dumps(change).encode("utf-8")
        auth = base64.b64encode(f"{self._username}:{self._password}".encode("utf-8")).decode(
            "ascii"
        )

        http_request = request.Request(
            url=endpoint,
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Basic {auth}",
            },
        )

        with request.urlopen(http_request, timeout=self._timeout_seconds) as response:
            response_body = response.read().decode("utf-8")

        parsed = json.loads(response_body)
        if not isinstance(parsed, dict):
            raise ValueError("ServiceNow response must be a JSON object.")

        return parsed
