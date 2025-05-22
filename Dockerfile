# Dockerfile for Airbnb Price Predictor API

# 1. Use a minimal Python image with Python 3.11
FROM python:3.10-slim

# Install system build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application code and trained model
COPY api/ ./api/
COPY models/ ./models/

# 5. Expose the port the app runs on
EXPOSE 8000

# 6. Launch the FastAPI app with Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]