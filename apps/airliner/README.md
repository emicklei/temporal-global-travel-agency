# airliner

Airliner application that uses the shared `converters` package and demonstrates a Temporal workflow for logging flight plans.

## Workflows

### LogFlightPlanWorkflow
A workflow that accepts a `FlightPlan` object and logs structured flight-plan data via `structlog`. Demonstrates how to work with complex typed input objects in Temporal workflows.

## Dependencies

- `converters`: Shared package for data conversion
- `structlog`: External package for structured logging

## Tests

- Includes a fixture-based test that loads JSON and constructs a generated `FlightPlan` model.
- Includes workflow tests that verify activity execution with proper inputs.

## Commands

From this directory:

```bash
make run
make test
make docker-build
make docker-run
```
