# Navigate to your repository directory
cd your-repo-directory

# Replace Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Install all required system dependencies including SSL libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libssl-dev \
    libffi-dev \
    ca-certificates \
    gcc \
    g++ \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Pre-download YOLOv10b model weights
RUN python -c "import ssl; ssl._create_default_https_context = ssl._create_unverified_context" && \
    python << 'EOF'
import os
os.environ['PYTHONHTTPSVERIFY'] = '0'
from ultralytics import YOLO
model = YOLO('yolov10b.pt')
print('Model downloaded successfully')
EOF

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health').read()" || exit 1

# Run the app
CMD exec gunicorn --bind 0.0.0.0:${PORT} --workers 1 --threads 4 --timeout 0 --access-logfile - app:app
EOF

# Replace requirements.txt
cat > requirements.txt << 'EOF'
flask==2.3.3
torch==2.0.1
torchvision==0.15.2
opencv-python==4.8.0.76
ultralytics==8.0.214
pillow==10.0.0
numpy==1.24.3
gunicorn==21.2.0
requests==2.31.0
certifi==2023.7.22
EOF

# Commit and push
git add Dockerfile requirements.txt
git commit -m "Fix: Resolve SSL library issues for model download - add libffi-dev, improve Python environment, add health check"
git push origin main
