ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim AS builder

# Use non-root for better security
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --locked

FROM python:${PYTHON_VERSION}-slim AS runtime

LABEL description="Notivae - Backend"
LABEL website="https://notivae.github.io/"

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY entrypoint.sh /
COPY alembic.ini ./
COPY alembic/ ./alembic
COPY app/ ./app

RUN chmod +x /entrypoint.sh && \
    adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost/healthz || exit 1

EXPOSE 80

ENV WEB_CONCURRENCY=4

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "app.main:app"]
