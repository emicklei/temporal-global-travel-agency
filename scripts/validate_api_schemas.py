#!/usr/bin/env python3
"""Validate all JSON schema files under apis/."""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_GLOB = "apis/**/*.schema.json"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_schema_files(repo_root: Path) -> list[Path]:
    return sorted(path for path in repo_root.glob(SCHEMA_GLOB) if path.is_file())


def validate_schema_file(schema_path: Path) -> list[str]:
    errors: list[str] = []

    try:
        content = schema_path.read_text(encoding="utf-8")
        parsed = json.loads(content)
    except OSError as exc:
        return [f"- {schema_path}: unable to read file ({exc})"]
    except json.JSONDecodeError as exc:
        return [
            f"- {schema_path}:{exc.lineno}:{exc.colno}: invalid JSON ({exc.msg})"
        ]

    if not isinstance(parsed, dict):
        errors.append(f"- {schema_path}: top-level JSON value must be an object")
        return errors

    schema_decl = parsed.get("$schema")
    if not isinstance(schema_decl, str) or not schema_decl:
        errors.append(f"- {schema_path}: missing or invalid '$schema' declaration")

    if parsed.get("type") != "object":
        errors.append(
            f"- {schema_path}: top-level 'type' must be 'object'"
        )

    properties = parsed.get("properties")
    required = parsed.get("required")
    if "properties" in parsed and not isinstance(properties, dict):
        errors.append(f"- {schema_path}: 'properties' must be an object")
    if "required" in parsed and not isinstance(required, list):
        errors.append(f"- {schema_path}: 'required' must be an array")

    if isinstance(properties, dict) and isinstance(required, list):
        missing_from_properties = [name for name in required if name not in properties]
        if missing_from_properties:
            joined = ", ".join(str(name) for name in missing_from_properties)
            errors.append(
                f"- {schema_path}: required fields missing from properties: {joined}"
            )

    return errors


def validate_all_schemas(repo_root: Path) -> list[str]:
    schema_files = discover_schema_files(repo_root)
    if not schema_files:
        return [f"- no schema files found matching {SCHEMA_GLOB}"]

    all_errors: list[str] = []
    for schema_file in schema_files:
        all_errors.extend(validate_schema_file(schema_file))
    return all_errors


def main() -> int:
    repo_root = get_repo_root()
    errors = validate_all_schemas(repo_root)

    if errors:
        print("Schema validation failed:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1

    count = len(discover_schema_files(repo_root))
    print(f"Schema validation passed for {count} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
