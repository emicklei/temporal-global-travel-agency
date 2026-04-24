from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _copy_generator_script(tmp_path: Path) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    source_script = repo_root / "scripts" / "tests" / "generate_api_models.sh"
    target_script = tmp_path / "scripts" / "tests" / "generate_api_models.sh"
    target_script.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_script, target_script)
    target_script.chmod(0o755)
    return target_script


def _write_schema2py_stub(bin_dir: Path) -> None:
    stub = bin_dir / "schema2py"
    stub.write_text(
        """#!/usr/bin/env bash
set -euo pipefail

schema=""
out=""
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -schema)
      schema="$2"
      shift 2
      ;;
    -out)
      out="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [[ -z "$schema" || -z "$out" ]]; then
  echo "missing -schema or -out" >&2
  exit 1
fi

mkdir -p "$(dirname "$out")"
printf '# generated from %s\n' "$schema" > "$out"
""",
        encoding="utf-8",
    )
    stub.chmod(0o755)


def test_generate_api_models_shell_generates_all_schema_outputs(tmp_path: Path) -> None:
    script = _copy_generator_script(tmp_path)

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
    assert "Generated 2 model file(s)." in result.stdout
    assert (
        tmp_path / "pkgs" / "generated" / "airliner" / "v1" / "flight_plan.py"
    ).exists()
    assert (
        tmp_path / "pkgs" / "generated" / "citytaxi" / "v2" / "taxi_plan.py"
    ).exists()


def test_generate_api_models_shell_fails_when_schema2py_is_missing(
    tmp_path: Path,
) -> None:
    script = _copy_generator_script(tmp_path)
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


def test_generate_api_models_shell_fails_when_no_schemas_exist(tmp_path: Path) -> None:
    script = _copy_generator_script(tmp_path)

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
