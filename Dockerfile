# Media Swarm - Production Dockerfile
# Multi-stage build with uv for fast dependency resolution

FROM python:3.12-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files first for caching
COPY pyproject.toml uv.lock* ./

# Install dependencies (cached layer)
RUN uv sync --no-dev --no-install-project

# Copy application code
COPY src/ src/
COPY docker/pgvector/ docker/pgvector/

# Install the project itself
RUN uv sync --no-dev

# Create output directories
RUN mkdir -p outputs logs

# Expose the AgentOS port
EXPOSE 7777

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7777/admin/health || exit 1

# Run the application
CMD ["uv", "run", "python", "-m", "src.app"]
