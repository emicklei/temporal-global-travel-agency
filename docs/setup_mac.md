## Setup

### Python

This is a Python monorepo scaffolded with `uv` and `pants`.
From the repository root:

```bash
brew install uv
uv sync --all-packages
curl -L -O https://pantsbuild.github.io/setup/pants && chmod +x pants
uv python install 3.9
```
Pants 2.17 boots with Python 3.9 and runs tests with Python 3.11 in this repository.

### Temporal

The repo defines multiple Temporal Workers.
For local developement, you need the temoral CLI.

    brew install temporal

### Model generation

The repo uses `schema2py` to (re)generate Python Pedantic models from JSON schemas.
This requires the [Go SDK](https://go.dev/doc/install) and the installation of `schema2py`.

    go install codeberg.org/emicklei/schema2py@latest