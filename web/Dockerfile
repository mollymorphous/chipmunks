# Official Node image, keep version in sync with .node-version
FROM docker.io/node:23.8.0-alpine@sha256:b2f1e6d2f9eaf82afc910ec1e3b14f2a252be3f91e661602017974dee1bd9f40 AS base
WORKDIR /app/

# Default to production for building
ENV NODE_ENV=production

# Create an unprivileged user app:app
RUN addgroup -S app && adduser -S app -G app

# Install dependencies (including dev dependencies for now)
COPY package.json package-lock.json /app/
RUN --mount=type=cache,target=/root/.npm/ \
    npm ci --include dev

# Make temp directories for Vite
RUN mkdir -p node_modules/.vite node_modules/.vite-temp && \
    chown -R app:app node_modules/.vite node_modules/.vite-temp

# Copy sources
COPY . /app/

# Expose HTTP port
EXPOSE 8080

# Development
FROM base AS dev
ENV NODE_ENV=development
# The app user needs write access for hot reloading
RUN chown -R app:app src *.html
USER app
CMD ["npm", "run", "dev", "--", "--host", "--port=8080"]

# Production
FROM base AS prod
RUN --network=none npm run build
USER app
CMD ["npm", "run", "preview", "--", "--host", "--port=8080"]
