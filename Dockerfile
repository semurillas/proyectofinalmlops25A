# Imagen base
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto al contenedor
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/main.py app/onnx_predictor.py ./

# Variable de entorno para FastAPI o Flask (modifica si es Flask)
ENV PORT=8000

# Comando para ejecutar la aplicación (FastAPI en este caso)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]