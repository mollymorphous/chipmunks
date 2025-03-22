# Stage 1: Base
# Official Node image, keep version in sync with .node-version
FROM docker.io/node:23.10.0-alpine@sha256:6eae672406a2bc8ed93eab6f9f76a02eb247e06ba82b2f5032c0a4ae07e825ba AS base

# Create an unprivileged user app:app
RUN addgroup -S app && adduser -S app -G app

# Set and expose app port, 8080 by default
ARG CHIPMUNKS_WEB_PORT=8080
EXPOSE ${CHIPMUNKS_WEB_PORT}
ENV PORT=${CHIPMUNKS_WEB_PORT}

# Best practice is to always set NODE_ENV=production
ENV NODE_ENV=production

# /app/ is the root of our code in the image
WORKDIR /app/

# Stage 2: Source files and dependencies, used for build and dev
FROM base AS source
COPY package.json package-lock.json /app/

# Install dev dependencies
RUN --mount=type=cache,target=/root/.npm/ \
    npm ci --include dev

# Copy sources
COPY . /app/

# Stage 3a: Development
FROM source AS dev

# The app user needs write access to /app/
RUN chown app:app /app/

# Run the development server as the unprivileged app user
USER app
ENV NODE_ENV=development
ENTRYPOINT [ "npm", "run", "dev", "--" ]

# Stage 3b: Build
FROM source AS build

# Build, assuming lint happened externally
RUN --mount=type=cache,target=/app/.next/cache/ \
    npm run build -- --no-lint

# Stage 4: Production
FROM base AS prod

# Ensure telemetry is disabled in production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy built standalone package and assets
COPY --from=build /app/public/ ./public/
COPY --from=build /app/.next/standalone/ ./ 
COPY --from=build /app/.next/static/ ./.next/static/

# Run the standalone server as the unprivileged app user
USER app
ENTRYPOINT [ "node", "server.js" ]
