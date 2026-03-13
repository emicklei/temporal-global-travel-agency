from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "install_workspace_deps.py"
SPEC = importlib.util.spec_from_file_location("install_workspace_deps", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
INSTALLER_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(INSTALLER_MODULE)


def test_dependency_name_parses_requirement_variants() -> None:
    assert INSTALLER_MODULE.dependency_name("converters") == "converters"
    assert INSTALLER_MODULE.dependency_name("requests>=2.0") == "requests"
    assert INSTALLER_MODULE.dependency_name("my-pkg[extra]>=1.0; python_version>='3.12'") == "my-pkg"


def test_resolve_install_target_prefers_local_workspace_package(tmp_path: Path) -> None:
    pkgs = tmp_path / "pkgs"
    (pkgs / "my_pkg").mkdir(parents=True)

    target = INSTALLER_MODULE.resolve_install_target("my-pkg>=1.0", pkgs)

    assert target == str(pkgs / "my_pkg")


def test_install_dependencies_uses_resolved_targets(tmp_path: Path, monkeypatch) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(
        """
[project]
dependencies = ["converters", "requests>=2"]
""".strip(),
        encoding="utf-8",
    )

    pkgs = tmp_path / "pkgs"
    (pkgs / "converters").mkdir(parents=True)

    captured_cmd = None

    def fake_run(command, check):
        nonlocal captured_cmd
        captured_cmd = command
        assert check is True

    monkeypatch.setattr(INSTALLER_MODULE.subprocess, "run", fake_run)

    INSTALLER_MODULE.install_dependencies(pyproject_path, pkgs)

    assert captured_cmd is not None
    assert captured_cmd[:5] == [
        INSTALLER_MODULE.sys.executable,
        "-m",
        "pip",
        "install",
        "--no-cache-dir",
    ]
    assert str(pkgs / "converters") in captured_cmd
    assert "requests>=2" in captured_cmd
