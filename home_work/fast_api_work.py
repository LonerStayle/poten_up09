from ultralytics import YOLO
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io, json
from functools import lru_cache

app = FastAPI()

@app.post("/yolo")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))  # PIL로 바로 변환
    results = model(img)
    datas = []
    result = results[0]
    boxes = result.boxes

    for box in boxes.data.tolist():
        datas.append(box)
    return json.dumps(datas)
