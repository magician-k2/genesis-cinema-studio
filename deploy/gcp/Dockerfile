# Dockerfile for GENESIS Cybernetic Brain OS on Google Cloud Run
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    APP_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY core/ ./core/
COPY web/ ./web/
COPY run_agentic_notebook.py ./

# Expose Cloud Run default port
EXPOSE 8080

# Run GENESIS Cognitive Mainframe Server
CMD ["python", "run_agentic_notebook.py", "--port", "8080"]
