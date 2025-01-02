FROM rasa/rasa-sdk:latest

# Switch to root user to install system dependencies
USER root

# Update the package list and install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set writable cache directories for Hugging Face
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HOME=/app/cache
RUN mkdir -p /app/cache && chmod -R 777 /app/cache

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Pre-download SentenceTransformer model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy the actions directory
COPY ./actions /app/actions

# Set the working directory
WORKDIR /app

# Switch back to non-root user
USER 1001

# Start the action server
CMD ["start", "--actions", "actions"]
