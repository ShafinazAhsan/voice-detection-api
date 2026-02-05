FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (FFmpeg is required for pydub to process audio)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port (Railway uses PORT environment variable)
EXPOSE 8000

# Start command (Using the modular list format is more robust)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
