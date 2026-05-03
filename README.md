# Global Travel Agency - a Temporal.io example

[![Tests and Coverage](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-tests-coverage.yml/badge.svg?branch=main)](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-tests-coverage.yml)
[![App Image From Tag](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-app-image-from-tag.yml/badge.svg)](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-app-image-from-tag.yml)
[![Coverage](https://codecov.io/gh/emicklei/temporal-global-travel-agency/branch/main/graph/badge.svg)](https://codecov.io/gh/emicklei/temporal-global-travel-agency)

## Structure

- `apps/`: application projects
- `apis/`: API contracts and schemas
- `pkgs/`: shared reusable packages 
- `pkgs/apis`: contains (generated) classes for API access
- `scripts/` : tools for local development

## Setup

This is a Python monorepo scaffolded with `uv` and `pants`.
From the repository root:

```bash
uv sync --all-packages
chmod +x ./pants
uv python install 3.9
```

Pants 2.17 boots with Python 3.9 and runs tests with Python 3.11 in this repository.

## App Commands

Each app has its own Makefile at `apps/<app name>/Makefile`.

For example, from `apps/airliner`:

```bash
make run
make test
make docker-build
make docker-run
```

## Docker Dependency Installation

App Dockerfiles install workspace dependencies from each app's
`pyproject.toml` using the shared script:

```bash
python scripts/install_workspace_deps.py --pyproject apps/<app>/pyproject.toml --packages-dir ./pkgs
```

## Run All Tests

```bash
PYTHON=python3.9 ./pants test ::
```

or simply:

```bash
./pants test ::
```

## Format And Validate

Run repository-wide formatting hooks from the root:

```bash
make fmt
```

Run repository validation checks separately:

```bash
make check
```

`make fmt` runs formatter hooks only (Ruff, whitespace, JSON formatting).
`make check` runs validation hooks only (schema validation, generated-model sync, tag format).

## Run Changed Tests

Run only tests affected by changes compared to `origin/main`:

```bash
PYTHON=python3.9 ./pants --changed-since=origin/main --changed-dependents=transitive test
```

## Pre-commit Hook: Tag Validation

This repository includes a local `pre-commit` hook that validates git tags follow:

```text
apps/<folder>/vX.Y.Z
```

Rules:

- `<folder>` must exist under `apps/`
- `X`, `Y`, and `Z` must be non-negative integers (`>= 0`)

Install and run:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## API Schema Validation

All JSON schema files under `apis/` are validated by:

- a local `pre-commit` hook (`validate-api-schemas`)
- the CI workflow (`Validate API JSON schemas` step)

For `apis/travelagent/v1/journey.schema.json`, each route `schema_version` must
match `<string>/v<integer>(.<integer>)*`, for example:

- `airliner/v1`
- `bikerental/v1.2`
- `citytaxi/v2.0`

Run manually from the repository root:

```bash
bash scripts/validate_api_schemas.sh
```

## API Model Generation

Generate Python Pydantic models for all schema files under `apis/`:

```bash
make gen
```

Generated files are written to `pkgs/apis/<domain>/<version>/`.
The `apis/` tree is schema-only and must not contain Python model files.
Generated files are committed to the repository and must stay in sync with schemas.

To verify generated models are up to date:

```bash
bash scripts/tests/generate_api_models.sh
git diff --exit-code -- pkgs/apis
```

The same generated-model sync check runs in pre-commit and CI.

Model files are generated with `codeberg.org/emicklei/schema2py` and include strict Pydantic validation behavior
as defined by each schema.

## Sparse checkouts
A monorepo will naturally grow quite large quite fast and for many reasons engineers will for the
most time prefer to only have a subset of the tree checked out at once. Git *sparse checkouts* provides
a mechanism for archieving this.

Executing:
```bash
git config core.sparseCheckout true
echo '/*'           >  .git/info/sparse-checkout
echo '!/apps/*'     >> .git/info/sparse-checkout
echo '/apps/travelagent/*' >> .git/info/sparse-checkout
```
enables sparse checkouts and configures git to checkout the the whole tree except all apps other
than `travelagent`. To make it happen, either run a checkout command or to update the work tree in-place:
```
git read-tree -mu HEAD
```
