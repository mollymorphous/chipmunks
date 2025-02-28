# Dependencies
#
# Official Python image, keep version in sync with .python-version
FROM docker.io/python:3.13.2-alpine@sha256:8a34ebceda7d48c11d6ec7f322807032f1f152ef121ea7f628cbd72643affd57 AS python
# Distroless uv image
FROM ghcr.io/astral-sh/uv:0.6.3@sha256:8257f3d17fd04794feaf89d83b4ccca3b2eaa5501de9399fa53929843c0a5b55 AS uv

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
COPY . /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    --network=none \
    uv sync --frozen --no-dev

# Stage 2: Runtime Base
FROM python AS base
WORKDIR /app/

# Create an unprivileged user app:app
RUN addgroup -S app && adduser -S app -G app

ENV PATH="/app/.venv/bin:$PATH"

# Configure Granian and expose port
EXPOSE 8080
ENV GRANIAN_PORT=8080 GRANIAN_HOST=0.0.0.0 GRANIAN_INTERFACE=asgi

COPY --from=build /app/ /app/

# Stage 3a: Development
FROM base AS dev
# The app user needs write access for hot reloading
RUN chown -R app:app /app/app
USER app
CMD ["granian", "app", "--reload"]

# Stage 3b: Production 
FROM base AS prod
USER app
CMD ["granian", "app"]
