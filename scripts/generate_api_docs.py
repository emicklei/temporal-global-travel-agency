#!/usr/bin/env python3
"""Generate HTML API documentation pages from JSON schemas in apis/."""

from __future__ import annotations

import html
import json
from pathlib import Path

SCHEMA_GLOB = "apis/**/*.schema.json"


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def discover_schema_files(repo_root: Path) -> list[Path]:
    return sorted(path for path in repo_root.glob(SCHEMA_GLOB) if path.is_file())


def output_path_for_schema(repo_root: Path, schema_path: Path) -> Path:
    relative = schema_path.relative_to(repo_root / "apis")
    if len(relative.parts) < 3:
        raise ValueError(f"Unexpected schema location: {schema_path}")

    output_name = relative.name.removesuffix(".schema.json") + ".html"
    return repo_root / "docs" / Path(*relative.parts[:-1]) / output_name


def format_type(property_schema: dict[str, object]) -> str:
    if "$ref" in property_schema and isinstance(property_schema["$ref"], str):
        return property_schema["$ref"]

    schema_type = property_schema.get("type")
    if isinstance(schema_type, list):
        return " | ".join(str(item) for item in schema_type)
    if isinstance(schema_type, str):
        if schema_type == "array":
            items = property_schema.get("items")
            if isinstance(items, dict):
                return f"array<{format_type(items)}>"
        return schema_type
    return "unknown"


def format_constraints(property_schema: dict[str, object]) -> str:
    constraints: list[str] = []

    for key in (
        "pattern",
        "format",
        "minLength",
        "maxLength",
        "minimum",
        "maximum",
        "minItems",
        "maxItems",
        "additionalProperties",
    ):
        if key in property_schema:
            value = property_schema[key]
            constraints.append(f"{key}={value!r}")

    enum_values = property_schema.get("enum")
    if isinstance(enum_values, list):
        constraints.append(f"enum={enum_values!r}")

    return ", ".join(constraints) if constraints else "-"


def render_properties_table(
    properties: dict[str, object],
    required_fields: set[str],
) -> str:
    if not properties:
        return "<p>No properties.</p>"

    rows: list[str] = []
    for name, schema_obj in properties.items():
        property_schema = schema_obj if isinstance(schema_obj, dict) else {}
        prop_type = html.escape(format_type(property_schema))
        required = "yes" if name in required_fields else "no"
        description = html.escape(str(property_schema.get("description", "-")))
        constraints = html.escape(format_constraints(property_schema))
        rows.append(
            "<tr>"
            f"<td><code>{html.escape(name)}</code></td>"
            f"<td><code>{prop_type}</code></td>"
            f"<td>{required}</td>"
            f"<td>{constraints}</td>"
            f"<td>{description}</td>"
            "</tr>"
        )

    return (
        "<table>"
        "<thead>"
        "<tr>"
        "<th>Property</th><th>Type</th><th>Required</th><th>Constraints</th><th>Description</th>"
        "</tr>"
        "</thead>"
        "<tbody>" + "".join(rows) + "</tbody></table>"
    )


def render_defs_section(defs: dict[str, object]) -> str:
    if not defs:
        return ""

    blocks: list[str] = ["<h2>$defs</h2>"]
    for name, def_obj in defs.items():
        def_schema = def_obj if isinstance(def_obj, dict) else {}
        schema_type = html.escape(format_type(def_schema))
        description = html.escape(str(def_schema.get("description", "")))

        blocks.append(f"<section><h3><code>{html.escape(name)}</code></h3>")
        blocks.append(f"<p><strong>Type:</strong> <code>{schema_type}</code></p>")
        if description:
            blocks.append(f"<p>{description}</p>")

        def_properties = def_schema.get("properties")
        def_required = def_schema.get("required")
        required_fields = (
            {item for item in def_required if isinstance(item, str)}
            if isinstance(def_required, list)
            else set()
        )
        if isinstance(def_properties, dict):
            blocks.append(render_properties_table(def_properties, required_fields))
        else:
            blocks.append(
                f"<p><strong>Constraints:</strong> {html.escape(format_constraints(def_schema))}</p>"
            )

        blocks.append("</section>")

    return "".join(blocks)


def render_schema_page(
    schema: dict[str, object], schema_path: Path, repo_root: Path
) -> str:
    title = str(schema.get("title", schema_path.stem.removesuffix(".schema")))
    description = str(schema.get("description", ""))
    schema_id = str(schema.get("$id", "-"))
    schema_type = str(schema.get("type", "-"))
    additional_props = schema.get("additionalProperties", True)

    properties = schema.get("properties")
    required = schema.get("required")
    defs = schema.get("$defs")

    property_map = properties if isinstance(properties, dict) else {}
    required_fields = (
        {item for item in required if isinstance(item, str)}
        if isinstance(required, list)
        else set()
    )
    defs_map = defs if isinstance(defs, dict) else {}

    relative_schema_path = schema_path.relative_to(repo_root)
    required_list = (
        "<ul>"
        + "".join(
            f"<li><code>{html.escape(name)}</code></li>"
            for name in sorted(required_fields)
        )
        + "</ul>"
        if required_fields
        else "<p>None</p>"
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} Schema Docs</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #4b5563;
      --border: #e5e7eb;
      --accent: #0f766e;
    }}
    body {{
      margin: 0;
      padding: 2rem;
      background: radial-gradient(circle at top right, #ecfeff, var(--bg) 45%);
      color: var(--text);
      font-family: ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif;
      line-height: 1.5;
    }}
    main {{
      max-width: 1080px;
      margin: 0 auto;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }}
    h1, h2, h3 {{ margin-top: 0; }}
    h1 {{ color: var(--accent); }}
    p.meta {{ color: var(--muted); margin-top: -0.25rem; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0 1.5rem 0; }}
    th, td {{ border: 1px solid var(--border); padding: 0.5rem; text-align: left; vertical-align: top; }}
    th {{ background: #f1f5f9; }}
    code {{ background: #f8fafc; padding: 0.1rem 0.3rem; border-radius: 4px; }}
    section {{ margin-bottom: 1.5rem; }}
  </style>
</head>
<body>
  <main>
    <h1>{html.escape(title)}</h1>
    <p class="meta">Source schema: <code>{html.escape(str(relative_schema_path))}</code></p>
    {f"<p>{html.escape(description)}</p>" if description else ""}

    <section>
      <h2>Overview</h2>
      <table>
        <tbody>
          <tr><th>$id</th><td><code>{html.escape(schema_id)}</code></td></tr>
          <tr><th>type</th><td><code>{html.escape(schema_type)}</code></td></tr>
          <tr><th>additionalProperties</th><td><code>{html.escape(str(additional_props))}</code></td></tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2>Required Fields</h2>
      {required_list}
    </section>

    <section>
      <h2>Properties</h2>
      {render_properties_table(property_map, required_fields)}
    </section>

    {render_defs_section(defs_map)}
  </main>
</body>
</html>
"""


def render_index_page(schema_docs: list[Path], docs_root: Path) -> str:
    groups: dict[str, list[tuple[str, str]]] = {}
    for doc_path in sorted(schema_docs):
        relative = doc_path.relative_to(docs_root)
        api_name = relative.parts[0]
        label = "/".join(relative.parts[1:])
        href = relative.as_posix()
        groups.setdefault(api_name, []).append((label, href))

    sections: list[str] = []
    for api_name in sorted(groups):
        items = "".join(
            f'<li><a href="{html.escape(href)}">{html.escape(label)}</a></li>'
            for label, href in groups[api_name]
        )
        sections.append(
            f"<section>"
            f"<h2>{html.escape(api_name)}</h2>"
            f"<ul>{items}</ul>"
            f"</section>"
        )

    body = "\n    ".join(sections)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>API Documentation</title>
  <style>
    :root {{
      --bg: #f8fafc;
      --panel: #ffffff;
      --text: #1f2937;
      --muted: #4b5563;
      --border: #e5e7eb;
      --accent: #0f766e;
    }}
    body {{
      margin: 0;
      padding: 2rem;
      background: radial-gradient(circle at top right, #ecfeff, var(--bg) 45%);
      color: var(--text);
      font-family: ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif;
      line-height: 1.5;
    }}
    main {{
      max-width: 860px;
      margin: 0 auto;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 1.5rem;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    }}
    h1 {{ color: var(--accent); margin-top: 0; }}
    h2 {{ margin-bottom: 0.25rem; }}
    ul {{ margin-top: 0.25rem; }}
    a {{ color: var(--accent); }}
  </style>
</head>
<body>
  <main>
    <h1>API Documentation</h1>
    {body}
  </main>
</body>
</html>
"""


def generate_docs(repo_root: Path) -> list[Path]:
    schema_docs: list[Path] = []
    for schema_path in discover_schema_files(repo_root):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        if not isinstance(schema, dict):
            raise ValueError(f"Schema must be a JSON object: {schema_path}")

        output_path = output_path_for_schema(repo_root, schema_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            render_schema_page(schema, schema_path, repo_root),
            encoding="utf-8",
        )
        schema_docs.append(output_path)

    docs_root = repo_root / "docs"
    index_path = docs_root / "api.html"
    docs_root.mkdir(parents=True, exist_ok=True)
    index_path.write_text(render_index_page(schema_docs, docs_root), encoding="utf-8")

    return schema_docs + [index_path]


def main() -> int:
    repo_root = get_repo_root()
    generated = generate_docs(repo_root)
    schema_count = len(generated) - 1  # exclude index
    print(
        f"Generated {schema_count} API schema page(s) + docs/api.html index in docs/."
    )
    for output in generated:
        print(output.relative_to(repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
