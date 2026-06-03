FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages for Docker version
RUN pip install --no-cache-dir \
    streamlit \
    pyshacl \
    rdflib

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY shacl/ ./shacl/
COPY ontology/ ./ontology/

# Create output directory
RUN mkdir -p output

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "scripts/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
