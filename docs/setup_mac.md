## Setup

### Python

This is a Python monorepo scaffolded with `uv` and `pants`.
From the repository root in Terminal:

```bash
brew install uv
uv sync --all-packages
curl -L -O https://pantsbuild.github.io/setup/pants && chmod +x pants
uv python install 3.9
```

Pants 2.17 boots with Python 3.9 and runs tests with Python 3.11 in this repository.

### Temporal

The repo defines multiple Temporal workers.
For local development, install the Temporal CLI:

```bash
brew install temporal
```

### Model generation

The repo uses `schema2py` to (re)generate Python Pydantic models from JSON schemas.
This requires the [Go SDK](https://go.dev/doc/install) and the installation of `schema2py`.

```bash
go install codeberg.org/emicklei/schema2py@latest
```

If `schema2py` is not found, add `$(go env GOPATH)/bin` to your `PATH`.
