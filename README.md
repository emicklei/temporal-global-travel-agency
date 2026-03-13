# Global Travel Agency - a Temporal.io example

[![Build Status](https://github.com/emicklei/temporal-python-monorepo/actions/workflows/ci-tests-coverage-and-app-image.yml/badge.svg?branch=main)](https://github.com/emicklei/temporal-python-monorepo/actions/workflows/ci-tests-coverage-and-app-image.yml)
[![Coverage](https://codecov.io/gh/emicklei/temporal-python-monorepo/branch/main/graph/badge.svg)](https://codecov.io/gh/emicklei/temporal-python-monorepo)

Python monorepo scaffolded with `uv` and `pants`.

## Structure

- `apps/`: application projects
- `apis/`: API contracts and schemas
- `apis/airliner/v1/flight_plan.schema.json`: JSON Schema for the `FlightPlan` object
- `apis/citytaxi/v1/taxi_plan.schema.json`: JSON Schema for the `TaxiPlan` object
- `apis/travelagent/v1/journey.schema.json`: JSON Schema for the `Journey` object
- `pkgs/`: shared reusable packages
- `apps/airliner`: application scaffolded from `demo-app` using `converters` and `quotes`
- `apps/citytaxi`: application scaffolded from `demo-app` using `converters` and `quotes`
- `apps/bikerental`: application scaffolded from `demo-app` using `converters` and `quotes`
- `apps/tourguide`: application scaffolded from `demo-app` using `converters` and `quotes`
- `apps/travelagent`: Temporal.io app with a hello-world workflow, worker, and starter

## Setup

From the repository root:

```bash
uv sync --all-packages
chmod +x ./pants
uv python install 3.9
```

Pants 2.17 boots with Python 3.9 and runs tests with Python 3.11 in this repository.

## Demo App Commands

The demo app has its own Makefile at `apps/demo-app/Makefile`.

From `apps/demo-app`:

```bash
make run
make test
make docker-build
make docker-run
```

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
# apps/demo-app
make test

# apps/airliner
make test

# apps/citytaxi
make test

# apps/bikerental
make test

# apps/tourguide
make test

# apps/travelagent
make test
```

Expected output for `make run`:

```text
24 degrees Celsius is 75.2 Fahrenheit
```

## Run All Tests

```bash
PYTHON=python3.9 ./pants test ::
```

or simply:

```bash
./pants test ::
```

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

Run manually from the repository root:

```bash
python scripts/validate_api_schemas.py
```

## API Model Generation

Generate Python dataclass models for all schema files under `apis/`:

```bash
make gen
```

Generated files are written to `pkgs/generated/<domain>/<version>/`.
Generated files are committed to the repository and must stay in sync with schemas.

To verify generated models are up to date:

```bash
python scripts/generate_api_models.py
git diff --exit-code -- pkgs/generated
```

The same generated-model sync check runs in pre-commit and CI.

Generated dataclasses include runtime validation in `__post_init__` for:

- required fields (`None` is rejected)
- JSON Schema type checks
- string constraints such as `pattern`, `minLength`, and `maxLength`
- RFC 3339 `date-time` format fields

Generated dataclasses also include an explicit `Validate()` instance method. This allows
calling validation manually after creating a model instance from parsed JSON or other
custom construction flows.
