from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

# Load model
model = YOLO('yolov10b.pt')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/detect', methods=['POST'])
def detect():
    """
    Endpoint for object detection
    Expects: JSON with base64 encoded image
    Returns: JSON with detections
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        # Get image from request
        image_file = request.files['image']
        image = Image.open(image_file)
        
        # Run inference
        results = model(image)
        
        # Parse results
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                detections.append({
                    'class': r.names[int(box.cls)],
                    'confidence': float(box.conf),
                    'bbox': box.xyxy.tolist()[0]
                })
        
        return jsonify({
            'detections': detections,
            'count': len(detections)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect-url', methods=['POST'])
def detect_url():
    """
    Endpoint for object detection from image URL
    Expects: JSON with 'url' field
    Returns: JSON with detections
    """
    try:
        data = request.get_json()
        if 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Run inference from URL
        results = model(data['url'])
        
        # Parse results
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                detections.append({
                    'class': r.names[int(box.cls)],
                    'confidence': float(box.conf),
                    'bbox': box.xyxy.tolist()[0]
                })
        
        return jsonify({
            'detections': detections,
            'count': len(detections)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
