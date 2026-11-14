FROM ubuntu:26.04

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates sudo zstd php8.5-cli wget git imagemagick \
 && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /usr/local/bin/

ARG PYTHON_VERSION=3.13
RUN uv python install ${PYTHON_VERSION}

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --all-extras --frozen --no-install-project
