FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (including SSL libraries)
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libssl-dev \
    ca-certificates \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Download YOLOv10b model weights
RUN python -c "from ultralytics import YOLO; YOLO('yolov10b.pt')"

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 app:app
