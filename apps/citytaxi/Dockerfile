FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /workspace \
    && python -m venv /opt/venv \
    && chown -R appuser:appuser /workspace /opt/venv

WORKDIR /workspace

# Copy workspace packages so local dependencies can be resolved from pyproject.
COPY --chown=appuser:appuser pkgs ./pkgs
COPY --chown=appuser:appuser scripts/install_workspace_deps.py ./scripts/install_workspace_deps.py
COPY --chown=appuser:appuser apps/citytaxi ./apps/citytaxi

USER appuser

RUN pip install --no-cache-dir --upgrade pip \
    && python ./scripts/install_workspace_deps.py --pyproject ./apps/citytaxi/pyproject.toml --packages-dir ./pkgs \
    && pip install --no-cache-dir --no-deps ./apps/citytaxi

WORKDIR /workspace/apps/citytaxi

CMD ["python", "-m", "citytaxi.main"]
