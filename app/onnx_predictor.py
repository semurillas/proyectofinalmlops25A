import boto3
import onnxruntime as ort
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = "model.onnx"

def download_model_from_s3(bucket_name, model_key):
    s3 = boto3.client("s3")
    if not os.path.exists(MODEL_PATH):
        s3.download_file(bucket_name, model_key, MODEL_PATH)

def load_model():
    session = ort.InferenceSession(MODEL_PATH)
    return session

def predict(session, input_array: np.ndarray):
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: input_array})[0]
    return int(np.argmax(result))  # si es clasificación de dígitos