# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    USE_SQLITE_FALLBACK=true

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create .venv64 virtual environment explicitly inside the Docker container
RUN python -m venv /app/.venv64

# Set environment PATH to use .venv64 binaries strictly
ENV PATH="/app/.venv64/bin:$PATH"

# Copy requirements first for better layer caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies inside .venv64
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY streamlit/ /app/streamlit/
COPY data/ /app/data/
COPY .env /app/.env

# Expose Streamlit default port
EXPOSE 8501

# Health check to ensure Streamlit server is active
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Command to run the application using .venv64 python/streamlit
CMD ["streamlit", "run", "streamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

