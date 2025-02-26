# Official Node image, keep version in sync with .node-version
FROM node:23.8.0-alpine@sha256:b2f1e6d2f9eaf82afc910ec1e3b14f2a252be3f91e661602017974dee1bd9f40 AS base

# Stage 1: Build
FROM base as build

# Install dependencies and cache them in their own layer
WORKDIR /build/
RUN --mount=type=cache,target=/root/.npm/ \
    --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    npm ci

# Add source files to the image and build distribution
ADD . /build/
RUN npm run build

# Stage 2: Runtime
FROM nginx:stable-alpine@sha256:cf5dfe2892b7ff58779be78bf9de1a4158c0158160dbf2956a56154e2e9407bd AS runtime

# Copy distribution from builder into the runtime nginx web root
COPY --from=build /build/dist/ /usr/share/nginx/html/
