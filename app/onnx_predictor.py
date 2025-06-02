import boto3               # Cliente AWS para acceder a servicios como S3
import onnxruntime as ort  # Librería para ejecutar modelos ONNX
import numpy as np         # Librería para manejo de matrices y vectores
import os                  # Para manejar archivos y rutas
from dotenv import load_dotenv  # Para cargar variables de entorno desde un archivo .env


load_dotenv()  # Cargar variables de entorno desde un archivo .env

LOCAL_MODEL_PATH = "model_onnx"  # Ruta local donde se guardará el modelo descargado

if os.path.exists(LOCAL_MODEL_PATH):
    os.remove(LOCAL_MODEL_PATH)  # Elimina el Modelo en local si ya existe

def download_model_from_s3(bucket_name, model_s3_path):
    """
    Descarga el modelo ONNX desde un bucket de S3 si no existe localmente.
    Argumentos:
     bucket_name = Nombre del bucket de S3
     model_s3_path = Ruta dentro del bucket donde se encuentra el modelo ONNX
    """
    s3 = boto3.client("s3")
    if not os.path.exists(LOCAL_MODEL_PATH):
        s3.download_file(bucket_name, model_s3_path, LOCAL_MODEL_PATH)

def load_model():
    """ 
    Carga el modelo ONNX desde la ruta local."
    Retorna una sesión de inferencia ONNX."
    """
    
    session = ort.InferenceSession(LOCAL_MODEL_PATH)
    return session

def predict(session, input_array: np.ndarray):
    """
    Realiza una predicción utilizando el modelo ONNX cargado.
    Argumentos: 
      session = Sesión de inferencia ONNX
      input_array = Array de entrada con las características del modelo
    
    Retorna la predicción del modelo.
    """
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: input_array})[0]
    return int(np.argmax(result))  # si es clasificación, devuelve la clase con mayor probabilidad