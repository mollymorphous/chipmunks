# Dependencies
#
# Official Python image, keep version in sync with .python-version
FROM docker.io/python:3.13.2-alpine@sha256:323a717dc4a010fee21e3f1aac738ee10bb485de4e7593ce242b36ee48d6b352 AS python
# Distroless uv image
FROM ghcr.io/astral-sh/uv:0.6.5@sha256:562193a4a9d398f8aedddcb223e583da394ee735de36b5815f8f1d22cb49be15 AS uv

# Stage 1: Build
FROM python AS build
WORKDIR /app/

# Install uv into the build worker
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0
COPY --from=uv /uv /uvx /bin/

# Install dependencies and cache them in their own layer
COPY pyproject.toml uv.lock /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Add source files to the image and run uv sync to compile bytecode
COPY --exclude=config.*.toml . /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    --network=none \
    uv sync --frozen --no-dev

# Stage 2: Runtime Base
FROM python AS base
WORKDIR /app/

# Create an unprivileged user app:app
RUN addgroup -S app && adduser -S app -G app

# Add virtual environment to path
ENV PATH="/app/.venv/bin:$PATH"

# Configure Granian and expose service
ARG CHIPMUNKS_API_PORT=8080
EXPOSE ${CHIPMUNKS_API_PORT}
ENV GRANIAN_PORT=${CHIPMUNKS_API_PORT} \
    GRANIAN_HOST=0.0.0.0 \
    GRANIAN_INTERFACE=asgi \
    GRANIAN_URL_PATH_PREFIX=/api/v1
ENTRYPOINT [ "granian", "app" ]

COPY --from=build /app/ /app/

# Stage 3a: Development
FROM base AS dev
COPY config.dev.toml /app/config.toml
USER app

# Stage 3b: Production 
FROM base AS prod
USER app
