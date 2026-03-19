# travelagent

Travelagent application using Temporal Python SDK with two example workflows for travel planning.

## Workflows

### HelloTravelWorkflow
A simple hello-world style workflow that greets a traveler by name.

### PrintJourneyWorkflow
A workflow that accepts a `Journey` object (with routes and travel details) and prints it as formatted JSON to the console. This demonstrates how to work with complex typed input objects in Temporal workflows.

## Commands

From this directory:

```bash
make run
make start
make test
make docker-build
make docker-run
```

## Local Temporal Server

The worker defaults to `localhost:7233` and namespace `default`.
Start a local Temporal dev server in another terminal if needed:

```bash
temporal server start-dev
```
