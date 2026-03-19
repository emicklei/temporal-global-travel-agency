# airliner

Airliner application that uses the shared `converters` package and demonstrates a Temporal workflow for logging flight plans.

## Workflows

### LogFlightPlanWorkflow
A workflow that accepts a `FlightPlan` object and logs its JSON representation using the shared `logger` activity. Demonstrates how to work with complex typed input objects in Temporal workflows.

## Dependencies

- `converters`: Shared package for data conversion
- `logger`: Shared package for logging data as JSON

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
