FROM python:3.12-slim

RUN apt update
# RUN apt update \
#     && apt install -y postgresql-client libpq-dev gcc \
#       && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN pip install pip poetry setuptools wheel -U --no-cache-dir

COPY pyproject.toml poetry.lock README.md .

RUN poetry install --no-cache

COPY app app

WORKDIR /usr/src/app/app

RUN poetry install --no-cache

EXPOSE 8000

CMD ["poetry", "run", "daphne", "-p", "8000", "-b", "0.0.0.0", "app.asgi:application"]
