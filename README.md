# YOLO-API-repo

A Flask-based REST API for real-time object detection using YOLOv10b model deployed on Google Cloud Run.

## Features

- Real-time object detection
- Multiple input methods: file upload, image URL, or base64 encoded images
- Lightweight and fast inference
- Deployed on Google Cloud Run with auto-scaling

## Endpoints

### Health Check
```bash
GET /health
