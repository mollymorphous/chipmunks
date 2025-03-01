# Stage 1: Base
# Official Node image, keep version in sync with .node-version
FROM docker.io/node:23.8.0-alpine@sha256:b2f1e6d2f9eaf82afc910ec1e3b14f2a252be3f91e661602017974dee1bd9f40 AS base

WORKDIR /app/

# Create an unprivileged user app:app
RUN addgroup -S app && adduser -S app -G app

COPY package.json package-lock.json /app/

# Stage 2: Development
# Install dependencies (including dev dependencies for now)
FROM base AS dev

# Switch to app user and chown /app/ for hot reloading
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

# Stage 3: Build
FROM dev AS build

# Install dev dependencies
RUN --mount=type=cache,target=/root/.npm/ \
    npm ci --include dev

# Copy sources
COPY . /app/

# Build distribution
RUN --network=none npm run build

# Stage 4: Production
FROM docker.io/nginx:1.27.4@sha256:4ff102c5d78d254a6f0da062b3cf39eaf07f01eec0927fd21e219d0af8bc0591 AS prod
COPY --from=build /app/dist /usr/share/nginx/html
