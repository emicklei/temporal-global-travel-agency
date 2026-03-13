#!/usr/bin/env python3
"""Install dependencies declared in a pyproject.toml.

Local workspace packages (under --packages-dir) are installed from path.
All other dependencies are installed by requirement spec.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
import tomllib


def dependency_name(requirement: str) -> str:
    """Extract the package name portion from a PEP 508 requirement string."""
    name = re.split(r"[<>=!~;\[\s]", requirement, maxsplit=1)[0]
    return name.strip()


def resolve_install_target(requirement: str, packages_dir: Path) -> str:
    """Resolve a dependency to a local path when available, else keep requirement."""
    name = dependency_name(requirement)
    if not name:
        return requirement

    candidates = [
        name,
        name.replace("-", "_"),
        name.lower(),
        name.lower().replace("-", "_"),
    ]

    for candidate in candidates:
        pkg_path = packages_dir / candidate
        if pkg_path.exists() and pkg_path.is_dir():
            return str(pkg_path)

    return requirement


def install_dependencies(pyproject_path: Path, packages_dir: Path) -> None:
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    dependencies = pyproject.get("project", {}).get("dependencies", [])

    if not isinstance(dependencies, list):
        raise ValueError("project.dependencies must be a list")

    install_targets = [resolve_install_target(dep, packages_dir) for dep in dependencies]
    if not install_targets:
        return

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", *install_targets],
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pyproject", required=True, help="Path to pyproject.toml")
    parser.add_argument(
        "--packages-dir",
        required=True,
        help="Path to workspace packages directory (e.g. ./pkgs)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    install_dependencies(Path(args.pyproject), Path(args.packages_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
