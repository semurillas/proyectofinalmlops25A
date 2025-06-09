from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from onnx_predictor import download_model_from_s3, load_model, predict
import numpy as np
import uvicorn
from logger import log_prediction_to_s3
import os


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración del modelo
BUCKET_NAME = "mlopsprojecbck"
MODEL_PATH = "model_onnx/mnist-12-int8.onnx"

download_model_from_s3(BUCKET_NAME, MODEL_PATH)
session = load_model()

class InputData(BaseModel):
    pixels: list[float]


@app.post("/predict")
async def predict_digit(data: InputData):
    try:
        if len(data.pixels) != 28 * 28:
            raise ValueError("La entrada debe tener exactamente 784 valores (28x28)")

        arr = np.array(data.pixels, dtype=np.float32).reshape(1, 1, 28, 28)
        pred = predict(session, arr)
        environment = os.getenv("ENVIRONMENT", "dev")  # Por defecto será 'dev'
        log_prediction_to_s3(str(pred), environment)
        return JSONResponse(content={"prediccion": pred})

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/health")
def health_check():
    return {"status": "ok"}
