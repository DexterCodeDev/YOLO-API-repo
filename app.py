import os
from fastapi import FastAPI, UploadFile, File
import uvicorn
import cv2
import numpy as np
from ultralytics import YOLO

app = FastAPI()

# Load model globally to cache it in the container's memory
model = YOLO('yolov10b.pt')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read and decode the uploaded image
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Run inference
    results = model(img)
    
    # Extract results
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidences = results[0].boxes.conf.tolist()
    
    return {
        "boxes": boxes, 
        "classes": classes, 
        "confidences": confidences
    }

if __name__ == "__main__":
    # Cloud Run requires binding to 0.0.0.0 and the injected PORT
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
