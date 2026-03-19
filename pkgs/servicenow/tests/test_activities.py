import json
from unittest.mock import patch

from temporalio.testing import ActivityEnvironment  # pants: no-infer-dep

from servicenow.activities import create_cmdb_change_activity


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def test_create_cmdb_change_activity_mocks_servicenow_api() -> None:
    env = ActivityEnvironment()
    fake_api_result = {
        "result": {
            "sys_id": "CHG0010001",
            "number": "CHG0010001",
            "state": "new",
        }
    }

    change = {
        "short_description": "Upgrade gateway cert",
        "description": "Rotate certificate before expiration.",
        "category": "software",
    }

    with patch(
        "servicenow.client.request.urlopen",
        return_value=_FakeResponse(fake_api_result),
    ) as mocked_urlopen:
        result = env.run(
            create_cmdb_change_activity,
            "https://acme.service-now.com",
            "integration-user",
            "top-secret",
            change,
        )

    assert result == fake_api_result
    mocked_urlopen.assert_called_once()
