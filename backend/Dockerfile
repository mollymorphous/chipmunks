# Official Python image, keep version in sync with .python-version
FROM docker.io/python:3.13.2-alpine@sha256:8a34ebceda7d48c11d6ec7f322807032f1f152ef121ea7f628cbd72643affd57 AS base

# Distroless uv, pinned here because Dependabot doesn't support COPY --from,
# see: https://github.com/dependabot/dependabot-core/issues/5103
FROM ghcr.io/astral-sh/uv:0.6.3@sha256:8257f3d17fd04794feaf89d83b4ccca3b2eaa5501de9399fa53929843c0a5b55 AS uv

# Stage 1: Build
FROM base AS build

# Install uv into the build worker
COPY --from=uv /uv /uvx /bin/

# Set up uv to compile bytecode at build time
ENV UV_COMPILE_BYTECODE=1 
# uv's package cache is mounted, so copy dependencies instead of linking them
ENV UV_LINK_MODE=copy
# Don't download Python with uv, we're getting Python from the official image
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app/

# Install dependencies and cache them in their own layer
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev

# Add source files to the image and run uv sync to compile bytecode
ADD . /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    --network=none \
    uv sync --frozen --no-dev

# Stage 2: Runtime
FROM base AS runtime

# Create an unprivileged user app:app
RUN addgroup -S app && adduser -S app -G app

# Copy app and venv into runtime image
COPY --from=build /app/ /app/

# Add venv to path
ENV PATH="/app/.venv/bin:$PATH"

# FastAPI listens on port 8000 by default
EXPOSE 8000

# Switch to unprivileged user
USER app

# Run FastAPI as an entrypoint, so additional CLI args can be appended to this
ENTRYPOINT ["fastapi", "run"]
