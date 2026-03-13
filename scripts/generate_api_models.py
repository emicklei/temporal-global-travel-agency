#!/usr/bin/env python3
"""Generate Python dataclass models from JSON schemas in apis/."""

from __future__ import annotations

import json
import keyword
from pathlib import Path

SCHEMA_GLOB = "apis/**/*.schema.json"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_schema_files(repo_root: Path) -> list[Path]:
    return sorted(path for path in repo_root.glob(SCHEMA_GLOB) if path.is_file())


def to_pascal_case(value: str) -> str:
    parts = [part for part in value.replace("-", "_").split("_") if part]
    return "".join(part[:1].upper() + part[1:] for part in parts)


def to_valid_identifier(value: str) -> str:
    candidate = value.replace("-", "_")
    if not candidate.isidentifier() or keyword.iskeyword(candidate):
        return f"{candidate}_"
    return candidate


def output_path_for_schema(repo_root: Path, schema_path: Path) -> Path:
    relative = schema_path.relative_to(repo_root / "apis")
    if len(relative.parts) < 3:
        raise ValueError(f"Unexpected schema location: {schema_path}")

    domain = relative.parts[0]
    version = relative.parts[1]
    schema_filename = relative.parts[-1]
    module_name = schema_filename.removesuffix(".schema.json")
    return repo_root / "pkgs" / "generated" / domain / version / f"{module_name}.py"


def class_name_for_schema(schema: dict[str, object], schema_path: Path) -> str:
    title = schema.get("title")
    if isinstance(title, str) and title:
        return to_pascal_case(title)
    return to_pascal_case(schema_path.name.removesuffix(".schema.json"))


def resolve_ref_type(ref_value: str) -> str:
    marker = "#/$defs/"
    if ref_value.startswith(marker):
        return to_pascal_case(ref_value.removeprefix(marker))
    raise ValueError(f"Unsupported $ref value: {ref_value}")


def schema_type_to_python(property_schema: dict[str, object]) -> str:
    ref_value = property_schema.get("$ref")
    if isinstance(ref_value, str):
        return resolve_ref_type(ref_value)

    schema_type = property_schema.get("type")
    if isinstance(schema_type, list):
        non_null = [entry for entry in schema_type if entry != "null"]
        if len(non_null) == 1 and isinstance(non_null[0], str):
            schema_type = non_null[0]

    if schema_type == "string":
        return "str"
    if schema_type == "integer":
        return "int"
    if schema_type == "number":
        return "float"
    if schema_type == "boolean":
        return "bool"
    if schema_type == "array":
        items = property_schema.get("items")
        if isinstance(items, dict):
            return f"list[{schema_type_to_python(items)}]"
        return "list[Any]"
    if schema_type == "object":
        return "dict[str, Any]"
    return "Any"


def render_dataclass(
    class_name: str,
    properties: dict[str, object],
    required: set[str],
) -> list[str]:
    lines = ["@dataclass(frozen=True)", f"class {class_name}:"]
    if not properties:
        lines.append("    pass")
        return lines

    for raw_name, value in properties.items():
        if not isinstance(value, dict):
            annotation = "Any"
        else:
            annotation = schema_type_to_python(value)

        field_name = to_valid_identifier(raw_name)
        if raw_name in required:
            lines.append(f"    {field_name}: {annotation}")
        else:
            lines.append(f"    {field_name}: {annotation} | None = None")
    return lines


def render_model_module(schema: dict[str, object], schema_path: Path) -> str:
    defs = schema.get("$defs")
    defs_mapping = defs if isinstance(defs, dict) else {}

    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise ValueError(f"Schema has no object properties: {schema_path}")

    required = schema.get("required")
    required_fields = (
        {name for name in required if isinstance(name, str)} if isinstance(required, list) else set()
    )

    output: list[str] = [
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from typing import Any",
        "",
    ]

    for def_name, def_schema in defs_mapping.items():
        if not isinstance(def_name, str) or not isinstance(def_schema, dict):
            continue

        target_class_name = to_pascal_case(def_name)
        def_properties = def_schema.get("properties")
        def_required = def_schema.get("required")

        if def_schema.get("type") == "object" and isinstance(def_properties, dict):
            required_set = (
                {name for name in def_required if isinstance(name, str)}
                if isinstance(def_required, list)
                else set()
            )
            output.extend(render_dataclass(target_class_name, def_properties, required_set))
        else:
            alias_type = schema_type_to_python(def_schema)
            output.append(f"{target_class_name} = {alias_type}")
        output.append("")

    root_name = class_name_for_schema(schema, schema_path)
    output.extend(render_dataclass(root_name, properties, required_fields))
    output.append("")

    return "\n".join(output).rstrip() + "\n"


def ensure_package_inits(base_dir: Path, model_dir: Path) -> None:
    current = base_dir
    while True:
        init_file = current / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding="utf-8")

        if current == model_dir:
            break
        if model_dir not in current.parents:
            break
        current = current.parent


def generate_models(repo_root: Path) -> list[Path]:
    schema_files = discover_schema_files(repo_root)
    generated_files: list[Path] = []

    base_generated_dir = repo_root / "pkgs" / "generated"
    for schema_file in schema_files:
        parsed = json.loads(schema_file.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError(f"Schema top-level must be an object: {schema_file}")

        output_path = output_path_for_schema(repo_root, schema_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        module_content = render_model_module(parsed, schema_file)
        output_path.write_text(module_content, encoding="utf-8")

        ensure_package_inits(output_path.parent, base_generated_dir)
        generated_files.append(output_path)

    return generated_files


def main() -> int:
    repo_root = get_repo_root()
    generated_files = generate_models(repo_root)

    if not generated_files:
        print(f"No schema files found matching {SCHEMA_GLOB}.")
        return 1

    print(f"Generated {len(generated_files)} model file(s):")
    for path in generated_files:
        print(f"- {path.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())