## Setup

### Python

This is a Python monorepo scaffolded with `uv` and `pants`.
From the repository root in PowerShell:

```powershell
winget install -e --id AstralSh.uv
uv sync --all-packages
Invoke-WebRequest -Uri https://pantsbuild.github.io/setup/pants -OutFile pants
uv python install 3.9
```

Pants 2.17 boots with Python 3.9 and runs tests with Python 3.11 in this repository.

### Temporal

The repo defines multiple Temporal workers.
For local development, install the Temporal CLI:

```powershell
irm https://temporal.download/cli.ps1 | iex
```

### Model generation

The repo uses `schema2py` to (re)generate Python Pydantic models from JSON schemas.
This requires the [Go SDK](https://go.dev/doc/install) and the installation of `schema2py`.

```powershell
winget install -e --id GoLang.Go
go install codeberg.org/emicklei/schema2py@latest
```

If `schema2py` is not found, add `%USERPROFILE%\\go\\bin` to your `Path`.
