import asyncio

import airliner.activities as activities_module
from airliner.activities import log_as_json


class _CaptureLogger:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def info(self, event: str, **kwargs) -> None:
        self.calls.append((event, kwargs))


def test_log_as_json_uses_structlog_info(monkeypatch) -> None:
    capture = _CaptureLogger()
    monkeypatch.setattr(activities_module, "logger", capture)

    asyncio.run(log_as_json("Flight plan", {"id": "fp-1"}))

    assert capture.calls == [
        ("flight_plan", {"message": "Flight plan", "data": {"id": "fp-1"}})
    ]
