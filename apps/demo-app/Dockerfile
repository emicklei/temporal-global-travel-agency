FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /workspace \
    && python -m venv /opt/venv \
    && chown -R appuser:appuser /workspace /opt/venv

WORKDIR /workspace

# Copy local workspace packages required by demo-app.
COPY --chown=appuser:appuser pkgs/converters ./pkgs/converters
COPY --chown=appuser:appuser pkgs/quotes ./pkgs/quotes
COPY --chown=appuser:appuser apps/demo-app ./apps/demo-app

USER appuser

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir ./pkgs/converters ./pkgs/quotes \
    && pip install --no-cache-dir --no-deps ./apps/demo-app

WORKDIR /workspace/apps/demo-app

CMD ["python", "-m", "demo_app.main"]
