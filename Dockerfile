FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=8080

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application packages
COPY agent_orchestrator /app/agent_orchestrator
COPY mcp_server_grc /app/mcp_server_grc
COPY static /app/static

# Run as non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["uvicorn", "mcp_server_grc.server:app", "--host", "0.0.0.0", "--port", "8080"]
