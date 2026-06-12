FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --group prod

COPY . .

RUN SECRET_KEY=build .venv/bin/python manage.py collectstatic --noinput

FROM python:3.14-slim


RUN useradd --uid 1500 --no-create-home app && \
    mkdir -p /tmp && chmod 1777 /tmp

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    TMPDIR=/dev/shm \
    HOME=/tmp

# try not to bust the cache...
# python dependencies
COPY --from=builder --chown=app:app /app/.venv .venv

# collected static files
COPY --from=builder --chown=app:app /app/staticfiles staticfiles

# app code and everything else
COPY --chown=app:app manage.py ./
COPY --chown=app:app monty_project monty_project
COPY --chown=app:app chumps/data chumps/data
COPY --chown=app:app chumps/management chumps/management
COPY --chown=app:app chumps/migrations chumps/migrations
COPY --chown=app:app chumps/templates chumps/templates
COPY --chown=app:app chumps/*.py chumps/

USER app

EXPOSE 8000

CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "--no-control-socket", "monty_project.wsgi:application", "--bind", "0.0.0.0:8000"]
