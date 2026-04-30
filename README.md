# Global Travel Agency - a Temporal.io example

[![Tests and Coverage](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-tests-coverage.yml/badge.svg?branch=main)](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-tests-coverage.yml)
[![App Image From Tag](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-app-image-from-tag.yml/badge.svg)](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-app-image-from-tag.yml)
[![Coverage](https://codecov.io/gh/emicklei/temporal-global-travel-agency/branch/main/graph/badge.svg)](https://codecov.io/gh/emicklei/temporal-global-travel-agency)

Python monorepo scaffolded with `uv` and `pants`.

## CI Trigger Policy

The `Tests and Coverage` workflow runs on:

- pull requests
- pushes to branches other than `main`

Direct pushes to `main` do not trigger this workflow.

## Structure

- `apps/`: application projects
- `apis/`: API contracts and schemas 
- `pkgs/`: shared reusable packages 

## Setup

From the repository root:

```bash
uv sync --all-packages
chmod +x ./pants
uv python install 3.9
```

Pants 2.17 boots with Python 3.9 and runs tests with Python 3.11 in this repository.

## Airliner App Commands

The airliner app has its own Makefile at `apps/airliner/Makefile`.

From `apps/airliner`:

```bash
make run
make test
make docker-build
make docker-run
```

## Citytaxi App Commands

The citytaxi app has its own Makefile at `apps/citytaxi/Makefile`.

From `apps/citytaxi`:

```bash
make run
make test
make docker-build
make docker-run
```

## Bikerental App Commands

The bikerental app has its own Makefile at `apps/bikerental/Makefile`.

From `apps/bikerental`:

```bash
make run
make test
make docker-build
make docker-run
```

## Tourguide App Commands

The tourguide app has its own Makefile at `apps/tourguide/Makefile`.

From `apps/tourguide`:

```bash
make run
make test
make docker-build
make docker-run
```

## Travelagent App Commands

The travelagent app has its own Makefile at `apps/travelagent/Makefile`.

From `apps/travelagent`:

```bash
make run
make start
make test
make docker-build
make docker-run
```

Travelagent tests include a fixture-driven journey validation case at
`apps/travelagent/tests/test_journey_fixture.py`, using
`apps/travelagent/tests/fixtures/plan1.json` which covers airliner, citytaxi,
and bikerental routes.

## Docker Dependency Installation

App Dockerfiles install workspace dependencies from each app's
`pyproject.toml` using the shared script:

```bash
python scripts/install_workspace_deps.py --pyproject apps/<app>/pyproject.toml --packages-dir ./pkgs
```

## Package Test Commands

Each package folder has a `Makefile` with a `test` target.

From each package folder:

```bash

# apps/airliner
make test

# apps/citytaxi
make test

# apps/bikerental
make test

# apps/tourguide
make test
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

## Coverage

Generate coverage with Pants:

```bash
PYTHON=python3.9 ./pants test --use-coverage ::
```

Reports are written to:

- `dist/coverage/python/coverage.xml`
- `dist/coverage/python/htmlcov/`

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

Generated files are written to `pkgs/generated/<domain>/<version>/`.
The `apis/` tree is schema-only and must not contain Python model files.
Generated files are committed to the repository and must stay in sync with schemas.

To verify generated models are up to date:

```bash
bash scripts/tests/generate_api_models.sh
git diff --exit-code -- pkgs/generated
```

The same generated-model sync check runs in pre-commit and CI.

Model files are generated with `schema2py` and include strict Pydantic validation behavior
as defined by each schema.

## API HTML Documentation Generation

Generate one HTML documentation page per JSON schema under `apis/`:

```bash
python scripts/generate_api_docs.py
```

Generated docs are written under `docs/` using the same path structure as `apis/`, for example:

- `apis/airliner/v1/flight_plan.schema.json` -> `docs/airliner/v1/flight_plan.html`
- `apis/bikerental/v1/bike_plan.schema.json` -> `docs/bikerental/v1/bike_plan.html`
- `apis/citytaxi/v1/taxi_plan.schema.json` -> `docs/citytaxi/v1/taxi_plan.html`

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
