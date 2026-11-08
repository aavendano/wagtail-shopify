# Base: previous Coolify nixpacks Ubuntu image already cached on this host.
# Avoids Docker Hub python pulls and Alpine+cargo (Rust) hangs observed in build.
FROM eqoeyswjjgu7xht2rpiwa7ya:240a051d9428c3392614b7527679b9244444435d

WORKDIR /app
USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    git \
    curl \
  && rm -rf /var/lib/apt/lists/* \
  && python3 -m venv /app/.venv

COPY requirements-prod.txt .
RUN /app/.venv/bin/pip install --upgrade pip \
  && /app/.venv/bin/pip install --no-cache-dir -r requirements-prod.txt

COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=3000 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

EXPOSE 3000

# Clear nixpacks ENTRYPOINT ["/bin/bash","-l","-c"]. With that entrypoint, a JSON
# Cmd array is parsed as bash -c SCRIPT $0 $1..., so only "./bin/daphne" runs and
# Daphne never receives "config.asgi:application".
ENTRYPOINT []
CMD ["bash", "-lc", "/app/.venv/bin/python manage.py migrate --noinput && exec ./bin/daphne -b 0.0.0.0 -p 3000 config.asgi:application"]
