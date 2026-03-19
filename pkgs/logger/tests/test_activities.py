import asyncio
import logging

from logger.activities import log_as_json


def test_log_as_json_writes_json_log(caplog) -> None:
    with caplog.at_level(logging.INFO):
        asyncio.run(log_as_json("test message", {"key": "value", "number": 42}))

    assert len(caplog.records) == 1
    assert "test message:" in caplog.text
    assert '"key": "value"' in caplog.text
    assert '"number": 42' in caplog.text
