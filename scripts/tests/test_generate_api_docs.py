from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "generate_api_docs.py"
SPEC = importlib.util.spec_from_file_location("generate_api_docs", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
DOCS_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCS_MODULE)

discover_schema_files = DOCS_MODULE.discover_schema_files
generate_docs = DOCS_MODULE.generate_docs
output_path_for_schema = DOCS_MODULE.output_path_for_schema
render_index_page = DOCS_MODULE.render_index_page
render_schema_page = DOCS_MODULE.render_schema_page


def test_discover_schema_files_lists_known_schemas() -> None:
    repo_root = Path(__file__).resolve().parents[2]

    schema_files = discover_schema_files(repo_root)

    assert schema_files
    assert repo_root / "apis/airliner/v1/flight_plan.schema.json" in schema_files
    assert repo_root / "apis/travelagent/v1/journey.schema.json" in schema_files


def test_output_path_for_schema_maps_to_docs_tree() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    schema_path = repo_root / "apis/citytaxi/v1/taxi_plan.schema.json"

    output_path = output_path_for_schema(repo_root, schema_path)

    assert output_path == repo_root / "docs/citytaxi/v1/taxi_plan.html"


def test_render_schema_page_contains_overview_properties_and_defs() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    schema_path = repo_root / "apis/demo/v1/demo.schema.json"
    schema = {
        "$id": "https://example.com/apis/demo/v1/demo.schema.json",
        "title": "DemoSchema",
        "description": "Demo API schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["id"],
        "properties": {
            "id": {"type": "string", "minLength": 3},
            "route": {"$ref": "#/$defs/Route"},
        },
        "$defs": {
            "Route": {
                "type": "object",
                "required": ["schema_version"],
                "properties": {
                    "schema_version": {
                        "type": "string",
                        "pattern": "^[^/]+/v[0-9]+$",
                    }
                },
            }
        },
    }

    html_page = render_schema_page(schema, schema_path, repo_root)

    assert "DemoSchema" in html_page
    assert "apis/demo/v1/demo.schema.json" in html_page
    assert "Required Fields" in html_page
    assert "schema_version" in html_page
    assert "$defs" in html_page


def test_generate_docs_writes_one_html_file_per_schema(tmp_path: Path) -> None:
    schema_path = tmp_path / "apis" / "demo" / "v1" / "trip.schema.json"
    schema_path.parent.mkdir(parents=True)
    schema_path.write_text(
        """
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/apis/demo/v1/trip.schema.json",
  "title": "Trip",
  "type": "object",
  "required": ["id"],
  "properties": {
    "id": {"type": "string"},
    "routes": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
""".strip(),
        encoding="utf-8",
    )

    generated = generate_docs(tmp_path)

    assert tmp_path / "docs" / "demo" / "v1" / "trip.html" in generated
    assert tmp_path / "docs" / "api.html" in generated


def test_render_index_page_contains_links_to_schema_docs(tmp_path: Path) -> None:
    docs_root = tmp_path / "docs"
    schema_docs = [
        docs_root / "airliner" / "v1" / "flight_plan.html",
        docs_root / "citytaxi" / "v1" / "taxi_plan.html",
    ]

    index_html = render_index_page(schema_docs, docs_root)

    assert "airliner" in index_html
    assert "airliner/v1/flight_plan.html" in index_html
    assert "citytaxi" in index_html
    assert "citytaxi/v1/taxi_plan.html" in index_html
    assert "API Documentation" in index_html
