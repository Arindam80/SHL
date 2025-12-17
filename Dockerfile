FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY datasets/ ./datasets/

# Create data directories
RUN mkdir -p data/raw data/processed data/embeddings experiments

# Build data and embeddings
RUN python src/scraper.py && \
    python src/data_pipeline.py && \
    python src/embeddings.py

# Expose port (7860 for HuggingFace, can be overridden)
EXPOSE 7860

# Environment variables
ENV PORT=7860
ENV USE_LLM_RERANKING=false
ENV EMBEDDING_MODEL=all-MiniLM-L6-v2

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860/health')"

# Start FastAPI server
CMD uvicorn src.api:app --host 0.0.0.0 --port ${PORT} --workers 1
