import json

from logger import LogRecord, append_log_record


def test_append_log_record_writes_single_json_line(tmp_path) -> None:
    log_file = tmp_path / "app.log"
    record = LogRecord(
        level="INFO",
        message="welcome to the airliner app!",
        logger_name="airliner",
        timestamp="2026-03-19T00:00:00Z",
    )

    append_log_record(log_file, record)

    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == {
        "timestamp": "2026-03-19T00:00:00Z",
        "level": "INFO",
        "message": "welcome to the airliner app!",
        "logger": "airliner",
    }


def test_append_log_record_appends_new_line_for_each_record(tmp_path) -> None:
    log_file = tmp_path / "app.log"

    append_log_record(
        log_file,
        LogRecord(
            level="INFO",
            message="first",
            logger_name="airliner",
            timestamp="2026-03-19T00:00:01Z",
        ),
    )
    append_log_record(
        log_file,
        LogRecord(
            level="INFO",
            message="second",
            logger_name="airliner",
            timestamp="2026-03-19T00:00:02Z",
        ),
    )

    lines = log_file.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["message"] == "first"
    assert json.loads(lines[1])["message"] == "second"


def test_log_record_to_dict_includes_context_when_present() -> None:
    record = LogRecord(
        level="ERROR",
        message="failed",
        logger_name="airliner",
        timestamp="2026-03-19T00:00:00Z",
        context={"request_id": "abc-123"},
    )

    assert record.to_dict() == {
        "timestamp": "2026-03-19T00:00:00Z",
        "level": "ERROR",
        "message": "failed",
        "logger": "airliner",
        "context": {"request_id": "abc-123"},
    }
