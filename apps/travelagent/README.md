# travelagent

Travelagent application using Temporal Python SDK with a hello-world style workflow.

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
