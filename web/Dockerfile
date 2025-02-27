# Official Node image, keep version in sync with .node-version
FROM node:23.8.0-alpine@sha256:b2f1e6d2f9eaf82afc910ec1e3b14f2a252be3f91e661602017974dee1bd9f40 AS base

WORKDIR /app/

# Create and switch to an unprivileged user app:app which owns /app/
RUN addgroup -S app && adduser -S app -G app && chown app:app /app/
USER app

EXPOSE 8080

# Install dependencies (including dev dependencies for now)
COPY --chown=app:app package.json package-lock.json /app/
RUN --mount=type=cache,target=/root/.npm/ \
    npm ci --include dev

# Copy sources
COPY --chown=app:app . /app/

# Development
FROM base AS dev
ENV NODE_ENV=development
CMD ["npm", "run", "dev", "--", "--host", "--port=8080"]

# Production
FROM base AS prod
RUN --network=none npm run build
ENV NODE_ENV=production
CMD ["npm", "run", "preview", "--", "--host", "--port=8080"]
