# Stage 1: Base
# Official Node image, keep version in sync with .node-version
FROM docker.io/node:23.9.0-alpine@sha256:dc4d20572e425f9d4c68a6f9c382fbcfec3fa2f8ef0b12cb1d96feabdb479a48 AS base

# Create an unprivileged user app:app
RUN addgroup -S app && adduser -S app -G app

WORKDIR /app/
COPY package.json package-lock.json /app/

# Stage 2: Build
FROM dev AS build

# Install dev dependencies
RUN --mount=type=cache,target=/root/.npm/ \
    npm ci --include dev

# Copy sources
COPY . /app/

# Build distribution
RUN --network=none npm run build

# Stage 3a: Development
FROM base AS dev
# The app user needs to own all of /app/ for hot reload and sync to work.
# This stage replicates some of the build stage steps as the app user to
# reduce intermediate layers.

RUN chown -R app:app /app/
USER app

# Install dev dependencies
RUN --mount=type=cache,target=/root/.npm/ \
    npm ci --include dev

# Copy sources
COPY --chown=app:app . /app/

# Expose Vite dev server
EXPOSE 8080
ENTRYPOINT [ "npm", "run", "dev", "--", "--host", "--port=8080" ]

# Stage 3b: Production
FROM docker.io/nginx:1.27.4@sha256:9d6b58feebd2dbd3c56ab5853333d627cc6e281011cfd6050fa4bcf2072c9496 AS prod
COPY --from=build /app/dist /usr/share/nginx/html
