# Proyecto Final MLOps 
## Junio - 2025
Este repositorio contiene el proyecto final de la materia **MLOps** desarrollado por Octavio Guerra y Sebastián Murillas. La solución se compone de un backend en FastAPI que sirve un modelo ONNX para reconocimiento de dígitos y de un frontend en Next.js que permite interactuar con el servicio.

Adicionalmente se han implementado pipelines (GitHub Actions) para el despliegue de las imagenes docker en las cuales se han contenerizado tanto los servicios de backend y frontend; este despliegue se realiza en dos ambientes uno en el entorno de desarrollo (dev) y otro en el de produccion (prod). El ambiente de desarrollo se despliega de manera local y el de produccion se despliega en AWS a traves de el servicio ECS y ECR. De acuerdo con los requerimientos solicitados el modelo ONNX utilizado se encuentra almcenado en un servicio de almacenamiento S3 en AWS, al cual se accede desde el contenedor de Backend, se descarga y instancia para su consumo. En el mismo repositorio S3 se almcenan las predicciones del modelo en archivos .txt que estan identificados de acuerdo al ambiente desde el cual se generan las predicciones.

## Modelo ONNX
El Modelo que usamos esta disponible en: https://github.com/onnx/models/tree/main/validated/vision/classification/mnist. Este Modelo clasifica un digito (0-9) escrito a mano y lo presenta en pantalla.

<img width="655" alt="image" src="https://github.com/user-attachments/assets/88e693ae-6c89-45d8-8d7f-832c5bf764cd" />

Este Modelo fue entrenando usando la librería de Imágenes de MNIST y esta basado en el uso de Redes Neuronales Convolucionales. Para mas detalle ver el enlace previo compartido.

## Estructura
- **app/**: código del backend (FastAPI, carga del modelo y logging de predicciones).
- **frontend-onnx/**: aplicación web creada con Next.js y TypeScript.
- **test/**: pruebas unitarias del modelo ONNX para ejecución desde el pipeline.
- **Dockerfile** en Raiz del repositorio. Para construir la imagen de Docker del Backend.
- **frontend-onnx/Dockerfile**: Para construir la imagen de Docker para frontend.
- **.github/workflows/**: flujos de trabajo de CI/CD para pruebas, construcción y despliegue en local (dev) y producción (AWS).

## Backend
El servicio en `app/main.py` expone dos endpoints:
- `POST /predict` recibe un arreglo de 784 valores (imagen 28x28) y devuelve la clase predicha por el modelo ONNX usado.
- `GET /health` para comprobación de estado, requerido para su despliegue en AWS ECS.

El modelo se descarga de un bucket AWS S3 (`mlopsprojecbck`) usando `app/onnx_predictor.py`. Las predicciones se registran en S3 mediante `app/logger.py`. La aplicación puede ejecutarse en local para dev:
```bash
docker run -p 8000:8000 -e ENVIRONMENT=dev -e AWS_ACCESS_KEY_ID=XXXXXXX -e AWS_SECRET_ACCESS_KEY=XXXXX -e AWS_REGION=us-east-2 onnx_model_dev:latest
En navegador ejecutar: http://localhost:8000
```
Y para prod:
```bash
En navegador ejecutar: http://alb-frontend-1245245350.us-east-2.elb.amazonaws.com
```

## Frontend
Dentro de `frontend-onnx` se encuentra una interfaz que permite subir imágenes o archivos JSON y mostrar la predicción obtenida del backend. El contenedor acepta la variable `NEXT_PUBLIC_BACKEND_URL` para indicar la URL del servicio del contenedor de backend para ser usado en local para dev y en ECS para prod.
El Contenedor de Frontend se puede ejecutar en local para dev:

```bash
docker run -p 3000:3000 -e AWS_ACCESS_KEY_ID=XXXX -e AWS_SECRET_ACCESS_KEY=XXXXXX -e AWS_REGION=us-east-2 frontend-dev:latest
En navegador ejecutar: http://localhost:3000
```
Y para prod:
```bash
En navegador ejecutar: http://alb-backend-predictor-1055852265.us-east-2.elb.amazonaws.com
```

## Pruebas
El archivo `test/test_onnx_model.py` descarga el modelo y un conjunto de datos de prueba desde S3 para validar que la precisión sea al menos del 80 %.
Las pruebas pueden ejecutarse con:
```bash
pytest test/test_onnx_model.py -v
```
Y se hacen tres (3) pruebas:
- Se le pasa un arreglo de valores (784) para que prediga un valor entre 0 y 9. Esto nos asegura que el modelo acepta valores y puede hacer predicción.
- Se le pasa un arreglo de valores (784) y su predicción ya establecida. Se compara la predicción que hace el modelo con la ya establecia y debe ser igual.
- Se le pasa un arreglo de varios valores y sus predicciones. Se compara la predicción que hace el modelo con los datos ya establecidos y se espera que acierte de al menos el 80%.

Con estas tres (3) pruebas aseguramos un Modelo operativo adecuado para hacer predicciones en Producción.

## Despliegue continuo
Los flujos definidos en `.github/workflows` ejecutan pruebas automáticas y generan imágenes Docker para backend y frontend. En la rama `prod` se publica la imagen en Amazon ECR y se actualiza el servicio en ECS.

## Uso de la Nube Pública AWS
- Amazon S3: Se utilizó como almacenamiento para alojar la imagen del modelo de inteligencia artificial en formato ONNX, seleccionada e integrada por nuestro equipo. Esta decisión está alineada con los requerimientos establecidos para el proyecto.
- Amazon ECS (Elastic Container Service): Se optó por este servicio de orquestación de contenedores debido a que permite desplegar y gestionar aplicaciones en contenedores sin necesidad de aprovisionar ni administrar servidores físicos o virtuales. ECS facilita la escalabilidad y simplifica el manejo de la infraestructura subyacente.
- Amazon ECR (Elastic Container Register). Donde se almacenaron las imagenes construidas de los contenedores para las aplicaciones frontend y backend.
- Amazon Load Balancer (ALB). Debido a que los contenedores o se exponen una IP Pública, que cambia cada vez que se hace redespliegue, creamos dos (2) Load Balancers. Uno para el Frontend y otro para el Backend. Estos al tener un nombre fijo, evita tener que hacer cambios al código, especificamente a la URL para cada uno de estos servicios. 


## Licencia
Este proyecto se distribuye bajo los términos de la licencia MIT.

## Autores

- Sebastian Murillas  
- Octavio Guerra M.
