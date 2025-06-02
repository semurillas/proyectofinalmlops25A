from fastapi import FastAPI
from pydantic import BaseModel
from onnx_predictor import download_model_from_s3, load_model, predict
import numpy as np

app = FastAPI()

# configuración
BUCKET_NAME = "mlopsprojecbck"
ONNX_MODEL = "model_onnx/mnist-12-int8.onnx"

download_model_from_s3(BUCKET_NAME, ONNX_MODEL)  # Descarga el modelo ONNX desde S3
session = load_model()

class InputData(BaseModel):
    pixels: list[float]  # o list[int], según el input del modelo

@app.post("/predict")
def predict_digit(data: InputData):
    arr = np.array(data.pixels, dtype=np.float32).reshape(1, 1, 28, 28)  # según el input esperado
    pred = predict(session, arr)
    return {"prediccion": pred}