#!/usr/bin/env python3
"""Generate Python Pydantic models from JSON schemas in apis/."""

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


def schema_allows_additional_properties(schema: dict[str, object]) -> bool:
    additional = schema.get("additionalProperties")
    if isinstance(additional, bool):
        return additional
    return True


def resolve_property_schema(
    property_schema: dict[str, object],
    defs_mapping: dict[str, object],
) -> dict[str, object]:
    ref_value = property_schema.get("$ref")
    if isinstance(ref_value, str) and ref_value.startswith("#/$defs/"):
        def_name = ref_value.removeprefix("#/$defs/")
        def_schema = defs_mapping.get(def_name)
        if isinstance(def_schema, dict):
            return def_schema
    return property_schema


def render_validator_method(
    raw_name: str,
    field_name: str,
    property_schema: dict[str, object],
    defs_mapping: dict[str, object],
) -> tuple[list[str], bool, bool]:
    resolved_schema = resolve_property_schema(property_schema, defs_mapping)

    min_length = resolved_schema.get("minLength")
    max_length = resolved_schema.get("maxLength")
    pattern = resolved_schema.get("pattern")
    fmt = resolved_schema.get("format")

    has_length_validation = isinstance(min_length, int) or isinstance(max_length, int)
    has_pattern_validation = isinstance(pattern, str) and bool(pattern)
    has_datetime_validation = fmt == "date-time"

    if not any(
        (has_length_validation, has_pattern_validation, has_datetime_validation)
    ):
        return [], False, False

    method_lines = [
        f'    @field_validator("{field_name}")',
        "    @classmethod",
        f"    def _validate_{field_name}(cls, value: str) -> str:",
    ]

    if has_length_validation:
        if isinstance(min_length, int):
            method_lines.append(f"        if len(value) < {min_length}:")
            method_lines.append(
                f'            raise ValueError("{raw_name} must be at least {min_length} characters")'
            )
        if isinstance(max_length, int):
            method_lines.append(f"        if len(value) > {max_length}:")
            method_lines.append(
                f'            raise ValueError("{raw_name} must be at most {max_length} characters")'
            )

    if has_pattern_validation:
        method_lines.append(f"        if re.fullmatch(r{pattern!r}, value) is None:")
        method_lines.append(
            f'            raise ValueError("{raw_name} does not match required pattern")'
        )

    if has_datetime_validation:
        method_lines.append("        try:")
        method_lines.append(
            "            datetime.fromisoformat(value.replace('Z', '+00:00'))"
        )
        method_lines.append("        except ValueError as error:")
        method_lines.append(
            f'            raise ValueError("{raw_name} must be RFC 3339 date-time") from error'
        )

    method_lines.append("        return value")
    return method_lines, has_pattern_validation, has_datetime_validation


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


def render_pydantic_model(
    class_name: str,
    properties: dict[str, object],
    required: set[str],
    defs_mapping: dict[str, object],
    allow_additional_properties: bool,
) -> tuple[list[str], bool, bool]:
    extra_mode = "allow" if allow_additional_properties else "forbid"
    lines = [
        f"class {class_name}(BaseModel):",
        f'    model_config = ConfigDict(extra="{extra_mode}", strict=True)',
    ]
    if not properties:
        return lines + ["    pass"], False, False

    uses_regex = False
    uses_datetime = False

    for raw_name, value in properties.items():
        property_schema = value if isinstance(value, dict) else {"type": "object"}
        annotation = schema_type_to_python(property_schema)

        field_name = to_valid_identifier(raw_name)
        default_expr = "" if raw_name in required else " = None"

        if field_name != raw_name:
            if raw_name in required:
                default_expr = f" = Field(alias={raw_name!r})"
            else:
                default_expr = f" = Field(default=None, alias={raw_name!r})"

        if raw_name in required:
            lines.append(f"    {field_name}: {annotation}{default_expr}")
        else:
            lines.append(f"    {field_name}: {annotation} | None{default_expr}")

    for raw_name, value in properties.items():
        property_schema = value if isinstance(value, dict) else {"type": "object"}
        field_name = to_valid_identifier(raw_name)
        method_lines, method_uses_regex, method_uses_datetime = render_validator_method(
            raw_name=raw_name,
            field_name=field_name,
            property_schema=property_schema,
            defs_mapping=defs_mapping,
        )
        if method_lines:
            lines.append("")
            lines.extend(method_lines)

        uses_regex = uses_regex or method_uses_regex
        uses_datetime = uses_datetime or method_uses_datetime

    return lines, uses_regex, uses_datetime


def render_model_module(schema: dict[str, object], schema_path: Path) -> str:
    defs = schema.get("$defs")
    defs_mapping = defs if isinstance(defs, dict) else {}

    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise ValueError(f"Schema has no object properties: {schema_path}")

    required = schema.get("required")
    required_fields = (
        {name for name in required if isinstance(name, str)}
        if isinstance(required, list)
        else set()
    )

    body_lines: list[str] = []
    needs_regex = False
    needs_datetime = False

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
            rendered_lines, uses_regex, uses_datetime = render_pydantic_model(
                target_class_name,
                def_properties,
                required_set,
                defs_mapping,
                schema_allows_additional_properties(def_schema),
            )
            body_lines.extend(rendered_lines)
            needs_regex = needs_regex or uses_regex
            needs_datetime = needs_datetime or uses_datetime
        else:
            alias_type = schema_type_to_python(def_schema)
            body_lines.append(f"{target_class_name} = {alias_type}")
        body_lines.append("")

    root_name = class_name_for_schema(schema, schema_path)
    rendered_root, uses_regex, uses_datetime = render_pydantic_model(
        root_name,
        properties,
        required_fields,
        defs_mapping,
        schema_allows_additional_properties(schema),
    )
    body_lines.extend(rendered_root)
    body_lines.append("")
    needs_regex = needs_regex or uses_regex
    needs_datetime = needs_datetime or uses_datetime

    output: list[str] = [
        "from __future__ import annotations",
        "",
    ]
    if needs_regex:
        output.append("import re")
    if needs_datetime:
        output.append("from datetime import datetime")
    output.extend(
        [
            "from typing import Any",
            "",
            "from pydantic import BaseModel, ConfigDict, Field, field_validator",
            "",
        ]
    )
    output.extend(body_lines)

    return "\n".join(output).rstrip() + "\n"


def generate_models(repo_root: Path) -> list[Path]:
    schema_files = discover_schema_files(repo_root)
    generated_files: list[Path] = []

    for schema_file in schema_files:
        parsed = json.loads(schema_file.read_text(encoding="utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError(f"Schema top-level must be an object: {schema_file}")

        output_path = output_path_for_schema(repo_root, schema_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        module_content = render_model_module(parsed, schema_file)
        output_path.write_text(module_content, encoding="utf-8")

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
