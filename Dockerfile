FROM python:3.10-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install wget to fetch weights
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bake weights into the image to prevent Cloud Run cold-start timeouts
RUN wget https://github.com/THU-MIG/yolov10/releases/download/v1.1/yolov10b.pt

COPY . .

CMD ["python", "app.py"]
