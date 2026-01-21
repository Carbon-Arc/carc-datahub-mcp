FROM python:3.10-slim

WORKDIR /app

# Install curl for healthcheck and uv for dependency management
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# Install dependencies (production only)
RUN uv sync --frozen --no-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port for SSE/HTTP transport
EXPOSE 8000

# Health check - verify server is listening on port 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -sf --max-time 5 http://localhost:8000/mcp -o /dev/null -w '' || exit 1

# Run the MCP server with SSE transport
CMD ["uv", "run", "mcp-server-datahub", "--transport", "http"]
