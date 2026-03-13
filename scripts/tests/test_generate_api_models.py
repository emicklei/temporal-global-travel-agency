from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "generate_api_models.py"
SPEC = importlib.util.spec_from_file_location("generate_api_models", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
GENERATOR_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATOR_MODULE)

discover_schema_files = GENERATOR_MODULE.discover_schema_files
generate_models = GENERATOR_MODULE.generate_models
output_path_for_schema = GENERATOR_MODULE.output_path_for_schema
render_model_module = GENERATOR_MODULE.render_model_module


def test_discover_schema_files_lists_known_schemas() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    schema_files = discover_schema_files(repo_root)

    assert schema_files
    assert repo_root / "apis/airliner/v1/flight_plan.schema.json" in schema_files
    assert repo_root / "apis/citytaxi/v1/taxi_plan.schema.json" in schema_files


def test_output_path_for_schema_maps_to_generated_pkg() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    schema_path = repo_root / "apis/airliner/v1/flight_plan.schema.json"

    output_path = output_path_for_schema(repo_root, schema_path)

    expected = repo_root / "pkgs/generated/airliner/v1/flight_plan.py"
    assert output_path == expected


def test_render_model_module_renders_defs_and_top_class() -> None:
    schema = {
        "title": "TaxiPlan",
        "type": "object",
        "required": ["id", "pick_address"],
        "properties": {
            "id": {"type": "string"},
            "pick_address": {"$ref": "#/$defs/Address"},
            "comment": {"type": "string"},
        },
        "$defs": {
            "Address": {
                "type": "object",
                "required": ["street"],
                "properties": {
                    "street": {"type": "string"},
                    "postal_code": {"type": "string"},
                },
            },
            "Timestampz": {"type": "string"},
        },
    }

    module_text = render_model_module(
        schema,
        Path("apis/citytaxi/v1/taxi_plan.schema.json"),
    )

    assert "class Address:" in module_text
    assert "Timestampz = str" in module_text
    assert "class TaxiPlan:" in module_text
    assert "pick_address: Address" in module_text
    assert "comment: str | None = None" in module_text


def test_generate_models_writes_output_and_package_inits(tmp_path: Path) -> None:
    schema_path = tmp_path / "apis" / "demo" / "v1" / "trip.schema.json"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(
        """
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Trip",
  "type": "object",
  "required": ["id"],
  "properties": {
    "id": {"type": "string"},
    "note": {"type": "string"}
  }
}
""".strip(),
        encoding="utf-8",
    )

    generated_files = generate_models(tmp_path)

    assert generated_files == [tmp_path / "pkgs/generated/demo/v1/trip.py"]
    model_text = generated_files[0].read_text(encoding="utf-8")
    assert "class Trip:" in model_text
    assert "id: str" in model_text
    assert "note: str | None = None" in model_text

    assert (tmp_path / "pkgs/generated/__init__.py").exists()
    assert (tmp_path / "pkgs/generated/demo/__init__.py").exists()
    assert (tmp_path / "pkgs/generated/demo/v1/__init__.py").exists()