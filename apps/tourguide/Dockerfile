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
COPY --chown=appuser:appuser apps/tourguide ./apps/tourguide

USER appuser

RUN pip install --no-cache-dir --upgrade pip \
    && python ./scripts/install_workspace_deps.py --pyproject ./apps/tourguide/pyproject.toml --packages-dir ./pkgs \
    && pip install --no-cache-dir --no-deps ./apps/tourguide

WORKDIR /workspace/apps/tourguide

CMD ["python", "-m", "tourguide.main"]
