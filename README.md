# temporal-global-travel-agency

[![Build Status](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-tests-coverage-and-app-image.yml/badge.svg?branch=main)](https://github.com/emicklei/temporal-global-travel-agency/actions/workflows/ci-tests-coverage-and-app-image.yml)
[![Coverage](https://codecov.io/gh/emicklei/temporal-global-travel-agency/branch/main/graph/badge.svg)](https://codecov.io/gh/emicklei/temporal-global-travel-agency)

Python monorepo scaffolded with `uv` and `pants`.

## Structure

- `apps/`: application projects
- `apis/`: API contracts and schemas
- `apis/airliner/v1/flight_plan.schema.json`: JSON Schema for the `FlightPlan` object
- `pkgs/`: shared reusable packages
- `pkgs/converters`: shared package exposing `DegreesToFahrenheit`
- `pkgs/quotes`: shared package exposing scientist quotes
- `apps/demo-app`: demo application using `converters` and `quotes`
- `apps/airliner`: application scaffolded from `demo-app` using `converters` and `quotes`
- `apps/citytaxi`: application scaffolded from `demo-app` using `converters` and `quotes`
- `apps/bikerental`: application scaffolded from `demo-app` using `converters` and `quotes`
- `apps/tourguide`: application scaffolded from `demo-app` using `converters` and `quotes`

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

# pkgs/converters
make test

# pkgs/quotes
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
