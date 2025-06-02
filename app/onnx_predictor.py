import os
from dotenv import load_dotenv  # Solo se usará en entorno local

import boto3                   # Cliente AWS para S3
import onnxruntime as ort      # Para ejecutar modelos ONNX
import numpy as np             # Para arrays numéricos

# Cargar .env solo en entorno local (no se usa en producción vía GitHub Actions)
load_dotenv()

# Cargar credenciales desde variables de entorno
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Ruta local del modelo
LOCAL_MODEL_PATH = "model_onnx"

# Eliminar el modelo local si ya existe (útil para pruebas limpias)
if os.path.exists(LOCAL_MODEL_PATH):
    os.remove(LOCAL_MODEL_PATH)

def download_model_from_s3(bucket_name, model_s3_path):
    """
    Descarga el modelo ONNX desde un bucket S3 si no existe localmente.
    Parámetros:
        bucket_name: Nombre del bucket en S3
        model_s3_path: Ruta del archivo ONNX dentro del bucket
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    if not os.path.exists(LOCAL_MODEL_PATH):
        s3.download_file(bucket_name, model_s3_path, LOCAL_MODEL_PATH)

def load_model():
    """
    Carga el modelo ONNX desde el archivo local.
    Retorna:
        Sesión ONNX para realizar inferencias.
    """
    session = ort.InferenceSession(LOCAL_MODEL_PATH)
    return session

def predict(session, input_array: np.ndarray):
    """
    Realiza una predicción con el modelo ONNX.
    Parámetros:
        session: sesión ONNX cargada
        input_array: numpy array con los datos de entrada
    Retorna:
        Predicción entera (índice de la clase predicha)
    """
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: input_array})[0]
    return int(np.argmax(result))  # Suponiendo tarea de clasificación