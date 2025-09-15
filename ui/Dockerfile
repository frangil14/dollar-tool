# Multi-stage build for optimized size and caching
FROM node:16-alpine as build

LABEL maintainer="dollar-tool" \
      description="Dollar Tool Frontend - Build Stage"

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production --silent \
    && npm cache clean --force

# Copy source code (only necessary files)
COPY src/ ./src/
COPY public/ ./public/

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine as production

LABEL maintainer="dollar-tool" \
      description="Dollar Tool Frontend - Production"

# Install wget for health check
RUN apk add --no-cache wget

# Create non-root user
RUN adduser -D -s /bin/sh -u 1000 nginx-user

# Copy React build from previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/server.conf /etc/nginx/conf.d/default.conf

# Create directories and set permissions
RUN mkdir -p /var/log/nginx \
    && mkdir -p /var/cache/nginx \
    && mkdir -p /tmp \
    && chown -R nginx-user:nginx-user /var/log/nginx \
    && chown -R nginx-user:nginx-user /usr/share/nginx/html \
    && chown -R nginx-user:nginx-user /var/cache/nginx \
    && chown -R nginx-user:nginx-user /tmp

USER nginx-user

EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
