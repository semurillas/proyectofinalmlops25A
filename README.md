# Proyecto Final MLOps 
## Junio - 2025
Este repositorio contiene el proyecto final de la materia **MLOps** desarrollado por Octavio Guerra y Sebastián Murillas. La solución se compone de un backend en FastAPI que sirve un modelo ONNX para reconocimiento de dígitos y de un frontend en Next.js que permite interactuar con el servicio.

## Estructura
- **app/**: código del backend (FastAPI, carga del modelo y logging de predicciones).
- **frontend-onnx/**: aplicación web creada con Next.js y TypeScript.
- **test/**: pruebas unitarias del modelo ONNX.
- **Dockerfile** y `frontend-onnx/Dockerfile`: imágenes de Docker para backend y frontend.
- **.github/workflows/**: flujos de trabajo de CI/CD para pruebas, construcción y despliegue en AWS.

## Backend
El servicio en `app/main.py` expone dos endpoints:
- `POST /predict` recibe un arreglo de 784 valores (imagen 28x28) y devuelve la clase predicha por el modelo.
- `GET /health` para comprobación de estado.

El modelo se descarga de un bucket S3 (`mlopsprojecbck`) usando `app/onnx_predictor.py`. Las predicciones se registran en S3 mediante `app/logger.py`. La aplicación puede ejecutarse con:
```bash
docker build -t onnx_predictor .
docker run -p 8000:8000 onnx_predictor
```

## Frontend
Dentro de `frontend-onnx` se encuentra una interfaz que permite subir imágenes o archivos JSON y mostrar la predicción obtenida del backend. El contenedor acepta la variable `NEXT_PUBLIC_BACKEND_URL` para indicar la URL del servicio.

## Pruebas
El archivo `test/test_onnx_model.py` descarga el modelo y un conjunto de datos de prueba desde S3 para validar que la precisión sea al menos del 80 %.
Las pruebas pueden ejecutarse con:
```bash
pytest test/test_onnx_model.py -v
```

## Despliegue continuo
Los flujos definidos en `.github/workflows` ejecutan pruebas automáticas y generan imágenes Docker para backend y frontend. En la rama `prod` se publica la imagen en Amazon ECR y se actualiza el servicio en ECS.

## Ejecución local
1. Instalar dependencias del backend:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
2. Iniciar el frontend:
   ```bash
   cd frontend-onnx
   npm install
   npm run dev
   ```
   La página estará disponible en `http://localhost:3000`.

## Licencia
Este proyecto se distribuye bajo los términos de la licencia MIT.

## Autores

- Sebastian Murillas  
- Octavio Guerra M.
