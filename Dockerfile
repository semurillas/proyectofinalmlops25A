# Imagen base
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY app/main.py app/onnx_predictor.py app/logger.py ./

# Variable de entorno por defecto (puede ser sobreescrita)
ENV PORT=8000

# Comando para ejecutar la app FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]