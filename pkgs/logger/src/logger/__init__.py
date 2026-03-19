from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any


@dataclass(slots=True)
class LogRecord:
    """Structured log record serialized as one JSON line."""

    level: str
    message: str
    logger_name: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    )
    context: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        record = {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "logger": self.logger_name,
        }
        if self.context is not None:
            record["context"] = self.context
        return record


def append_log_record(file_path: str | Path, record: LogRecord) -> None:
    """Append one JSON log record to the target file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")
