FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
RUN uv sync

COPY app .

EXPOSE 8000
CMD ["daphne", "-p", "8000", "-b", "0.0.0.0", "main:app"]
