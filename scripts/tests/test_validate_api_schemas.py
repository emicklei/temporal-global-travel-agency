from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "validate_api_schemas.py"
SPEC = importlib.util.spec_from_file_location("validate_api_schemas", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
VALIDATOR_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR_MODULE)

discover_schema_files = VALIDATOR_MODULE.discover_schema_files
validate_all_schemas = VALIDATOR_MODULE.validate_all_schemas
validate_schema_file = VALIDATOR_MODULE.validate_schema_file


def test_discover_schema_files_lists_known_schemas() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    schema_files = discover_schema_files(repo_root)

    assert schema_files
    assert repo_root / "apis/airliner/v1/flight_plan.schema.json" in schema_files


def test_validate_schema_file_reports_non_object_top_level(tmp_path: Path) -> None:
    schema_path = tmp_path / "bad.schema.json"
    schema_path.write_text('[]', encoding="utf-8")

    errors = validate_schema_file(schema_path)

    assert len(errors) == 1
    assert "top-level JSON value must be an object" in errors[0]


def test_validate_schema_file_reports_malformed_json(tmp_path: Path) -> None:
    schema_path = tmp_path / "broken.schema.json"
    schema_path.write_text('{"$schema": ', encoding="utf-8")

    errors = validate_schema_file(schema_path)

    assert len(errors) == 1
    assert "invalid JSON" in errors[0]


def test_validate_schema_file_required_must_exist_in_properties(tmp_path: Path) -> None:
    schema_path = tmp_path / "invalid_required.schema.json"
    schema_path.write_text(
        """
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id", "name"],
  "properties": {
    "id": {"type": "string"}
  }
}
""".strip(),
        encoding="utf-8",
    )

    errors = validate_schema_file(schema_path)

    assert len(errors) == 1
    assert "required fields missing from properties: name" in errors[0]


def test_validate_all_schemas_passes_for_temp_valid_schema_tree(tmp_path: Path) -> None:
    schema_path = tmp_path / "apis" / "sample" / "v1" / "sample.schema.json"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(
        """
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["id"],
  "properties": {
    "id": {"type": "string"}
  }
}
""".strip(),
        encoding="utf-8",
    )

    errors = validate_all_schemas(tmp_path)

    assert errors == []
