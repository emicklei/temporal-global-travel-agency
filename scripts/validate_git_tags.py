#!/usr/bin/env python3
"""Validate repository tags follow apps/<folder>/vX.Y.Z and folder exists."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TAG_PATTERN = re.compile(r"^apps/([^/]+)/v(\d+)\.(\d+)\.(\d+)$")


def get_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def list_tags(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "tag", "--list"],
        check=True,
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def list_app_folders(repo_root: Path) -> set[str]:
    apps_dir = repo_root / "apps"
    if not apps_dir.is_dir():
        return set()
    return {
        child.name
        for child in apps_dir.iterdir()
        if child.is_dir() and not child.name.startswith(".")
    }


def validate_tags(tags: list[str], app_folders: set[str]) -> list[str]:
    errors: list[str] = []
    for tag in tags:
        match = TAG_PATTERN.match(tag)
        if not match:
            errors.append(
                f"- {tag}: does not match required pattern apps/<folder>/vX.Y.Z with non-negative integer X,Y,Z"
            )
            continue

        folder = match.group(1)
        if folder not in app_folders:
            errors.append(
                f"- {tag}: folder '{folder}' does not exist under apps/"
            )

    return errors


def main() -> int:
    try:
        repo_root = get_repo_root()
    except subprocess.CalledProcessError as exc:
        print(f"Unable to determine repository root: {exc}", file=sys.stderr)
        return 1

    try:
        tags = list_tags(repo_root)
    except subprocess.CalledProcessError as exc:
        print(f"Unable to list git tags: {exc}", file=sys.stderr)
        return 1

    if not tags:
        print("No git tags found; tag format check passed.")
        return 0

    app_folders = list_app_folders(repo_root)
    errors = validate_tags(tags, app_folders)
    if errors:
        print("Invalid git tag(s) detected:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("All git tags match apps/<folder>/vX.Y.Z and reference an existing apps folder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
