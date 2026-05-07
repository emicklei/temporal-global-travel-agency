import asyncio
import logging
import random

from logger.activities import log_as_json


def test_log_as_json_writes_json_log(caplog, monkeypatch) -> None:
    async def fake_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(random, "random", lambda: 0.0)

    with caplog.at_level(logging.INFO):
        asyncio.run(log_as_json("test message", {"key": "value", "number": 42}))

    assert len(caplog.records) == 2
    assert "Simulating traveling, sleep for" in caplog.text
    assert "test message:" in caplog.text
    assert '"key": "value"' in caplog.text
    assert '"number": 42' in caplog.text
