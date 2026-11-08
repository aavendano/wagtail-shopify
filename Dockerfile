FROM python:3.12-slim-bookworm

WORKDIR /app

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /app/.venv \
  && /app/.venv/bin/pip install --upgrade pip \
  && /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=3000 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

EXPOSE 3000

CMD ["./bin/daphne", "-b", "0.0.0.0", "-p", "3000", "config.asgi:application"]
