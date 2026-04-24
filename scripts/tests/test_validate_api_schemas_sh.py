from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _copy_validator_script(tmp_path: Path) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    source_script = repo_root / "scripts" / "validate_api_schemas.sh"
    target_script = tmp_path / "scripts" / "validate_api_schemas.sh"
    target_script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_script, target_script)
    target_script.chmod(0o755)
    return target_script


def _write_schema2py_stub(bin_dir: Path) -> None:
    stub = bin_dir / "schema2py"
    stub.write_text(
        """#!/usr/bin/env bash
set -euo pipefail

validate=false
schema=""
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -validate)
      validate=true
      shift
      ;;
    -schema)
      schema="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [[ "$validate" != true || -z "$schema" ]]; then
  echo "missing -validate or -schema" >&2
  exit 1
fi

python - <<'PY' "$schema"
import json
import sys
from pathlib import Path

schema_path = Path(sys.argv[1])
try:
    content = schema_path.read_text(encoding="utf-8")
    parsed = json.loads(content)
except json.JSONDecodeError as exc:
    print(f"invalid JSON: {exc.msg}", file=sys.stderr)
    raise SystemExit(1)

if not isinstance(parsed, dict):
    print("top-level JSON value must be an object", file=sys.stderr)
    raise SystemExit(1)
PY
""",
        encoding="utf-8",
    )
    stub.chmod(0o755)


def test_validate_api_schemas_shell_validates_all_schema_files(tmp_path: Path) -> None:
    script = _copy_validator_script(tmp_path)

    (tmp_path / "apis" / "airliner" / "v1").mkdir(parents=True)
    (tmp_path / "apis" / "citytaxi" / "v2").mkdir(parents=True)
    (tmp_path / "apis" / "airliner" / "v1" / "flight_plan.schema.json").write_text(
        "{}", encoding="utf-8"
    )
    (tmp_path / "apis" / "citytaxi" / "v2" / "taxi_plan.schema.json").write_text(
        "{}", encoding="utf-8"
    )

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _write_schema2py_stub(bin_dir)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"

    result = subprocess.run(
        ["bash", str(script)],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "Schema validation passed for 2 file(s)." in result.stdout


def test_validate_api_schemas_shell_fails_when_schema2py_is_missing(tmp_path: Path) -> None:
    script = _copy_validator_script(tmp_path)
    (tmp_path / "apis" / "demo" / "v1").mkdir(parents=True)
    (tmp_path / "apis" / "demo" / "v1" / "trip.schema.json").write_text(
        "{}", encoding="utf-8"
    )

    result = subprocess.run(
        ["bash", str(script)],
        cwd=tmp_path,
        env={"PATH": "/usr/bin:/bin"},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "schema2py not found on PATH" in result.stderr


def test_validate_api_schemas_shell_fails_for_invalid_schema(tmp_path: Path) -> None:
    script = _copy_validator_script(tmp_path)

    (tmp_path / "apis" / "demo" / "v1").mkdir(parents=True)
    (tmp_path / "apis" / "demo" / "v1" / "trip.schema.json").write_text(
        "[]", encoding="utf-8"
    )

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _write_schema2py_stub(bin_dir)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"

    result = subprocess.run(
        ["bash", str(script)],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "top-level JSON value must be an object" in result.stderr


def test_validate_api_schemas_shell_fails_when_no_schemas_exist(tmp_path: Path) -> None:
    script = _copy_validator_script(tmp_path)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _write_schema2py_stub(bin_dir)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"

    result = subprocess.run(
        ["bash", str(script)],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "No schema files found under apis/." in result.stderr