
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for models and data
RUN mkdir -p /app/models /app/data /app/uploads

# Download and prepare ML models (placeholder)
RUN echo "Downloading ML models..." && \
    mkdir -p /app/models/whisper-malayalam && \
    mkdir -p /app/models/yolo-crop-disease && \
    mkdir -p /app/models/llama2-7b-kerala-agri

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "fastapi_backend:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
