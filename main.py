from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()
model = YOLO("yolov10n.pt") # Automatically downloads weights

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Fixed: Use frombuffer instead of fromstring to handle modern numpy operations safely
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    results = model(img)
    return {"boxes": results[0].boxes.xyxy.tolist()}
