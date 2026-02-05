FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Railway provides the PORT environment variable. 
# We use shell form (no brackets) so the $PORT variable is resolved correctly.
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
