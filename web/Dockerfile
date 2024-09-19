FROM python:3.12-slim
RUN apt update \
    && apt install -y postgresql-client libpq-dev gcc \
      && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
