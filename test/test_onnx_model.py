import json
import boto3
import os
import numpy as np
import onnxruntime as ort
import pytest

# --- Configuración ---
BUCKET_NAME = "mlopsprojecbck"
MODEL_KEY = "model_onnx/mnist-12-int8.onnx"
TEST_DATA_KEY = "test_data/test_data.json"
MODEL_LOCAL_PATH = "model_onnx"
TEST_DATA_LOCAL_PATH = "test_data.json"

if os.path.exists(MODEL_LOCAL_PATH):
    os.remove(MODEL_LOCAL_PATH)  # Elimina el modelo en local si ya existe
if os.path.exists(TEST_DATA_LOCAL_PATH):
    os.remove(TEST_DATA_LOCAL_PATH)  # Elimina los datos de prueba en local si ya existen

# --- Descarga desde S3 ---
def download_from_s3(bucket, key, destination):
    if not os.path.exists(destination):
        s3 = boto3.client("s3")
        s3.download_file(bucket, key, destination)

download_from_s3(BUCKET_NAME, MODEL_KEY, MODEL_LOCAL_PATH)
download_from_s3(BUCKET_NAME, TEST_DATA_KEY, TEST_DATA_LOCAL_PATH)

# --- Carga modelo y datos ---
session = ort.InferenceSession(MODEL_LOCAL_PATH)

def predict(input_array: np.ndarray):
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: input_array})[0]
    return int(np.argmax(result))

with open(TEST_DATA_LOCAL_PATH, "r") as f:
    test_data = json.load(f)

# --- Pruebas con Pytest ---
def test_prediction_format():
    """El modelo responde correctamente con un input válido."""
    sample = test_data[0]
    arr = np.array(sample["pixels"], dtype=np.float32).reshape(1, 1, 28, 28)
    pred = predict(arr)
    assert isinstance(pred, int)
    assert 0 <= pred <= 9

def test_known_prediction():
    """El modelo predice correctamente para un caso conocido."""
    sample = test_data[1]
    arr = np.array(sample["pixels"], dtype=np.float32).reshape(1, 1, 28, 28)
    pred = predict(arr)
    assert pred == sample["label"]

def test_overall_accuracy():
    """La precisión del modelo debe ser al menos 80% en el conjunto de prueba."""
    correct = 0
    for sample in test_data:
        arr = np.array(sample["pixels"], dtype=np.float32).reshape(1, 1, 28, 28)
        pred = predict(arr)
        if pred == sample["label"]:
            correct += 1
    accuracy = correct / len(test_data)
    print(f"\nPrecisión del modelo: {accuracy:.2%}")
    assert accuracy >= 0.80