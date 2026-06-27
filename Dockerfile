FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    libz-dev libjpeg-dev libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --group prod

COPY . .

RUN SECRET_KEY=build .venv/bin/python manage.py collectstatic --noinput && \
    find /app -maxdepth 2 -name 'static' -type d -exec rm -rf {} + && \
    chmod +x /app/entrypoint.sh

FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --uid 1500 --no-create-home app && \
    mkdir -p /tmp && chmod 1777 /tmp

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    TMPDIR=/dev/shm \
    HOME=/tmp

COPY --from=builder --chown=app:app /app/.venv .venv
COPY --from=builder --chown=app:app /app/staticfiles staticfiles
COPY --from=builder --chown=app:app /app/entrypoint.sh .
COPY --from=builder --chown=app:app /app/manage.py .
COPY --from=builder --chown=app:app /app/monty_project monty_project
COPY --from=builder --chown=app:app /app/chumps chumps
COPY --from=builder --chown=app:app /app/guestbook guestbook

USER app

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
