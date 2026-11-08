# Use alpine (already present on this host) to avoid Docker Hub pull timeouts.
FROM alpine:3.24

WORKDIR /app

RUN apk add --no-cache \
      bash \
      build-base \
      cargo \
      curl \
      git \
      libffi-dev \
      openssl-dev \
      postgresql-dev \
      python3 \
      python3-dev \
      py3-pip \
  && python3 -m venv /app/.venv

COPY requirements.txt .
RUN /app/.venv/bin/pip install --upgrade pip \
  && /app/.venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=3000 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

EXPOSE 3000

CMD ["./bin/daphne", "-b", "0.0.0.0", "-p", "3000", "config.asgi:application"]
