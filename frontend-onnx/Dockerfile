# Etapa 1: Construcción
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Etapa 2: Producción
FROM node:18-alpine

WORKDIR /app

# Copiar archivos de compilación
COPY --from=builder /app/.next .next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./

# Instalar dependencias necesarias para producción
RUN npm install --omit=dev

# Variable de entorno por si quieres cambiar el puerto desde ECS o GitHub Actions
ENV PORT=3000

EXPOSE 3000

# Usa el script de package.json que ya maneja -p y -H
CMD ["npm", "start"]
