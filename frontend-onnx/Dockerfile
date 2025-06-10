# Etapa 1: Construcción
FROM node:18-alpine AS builder

WORKDIR /app

# Declarar la variable que se pasará desde GitHub Actions
ARG NEXT_PUBLIC_BACKEND_URL
ENV NEXT_PUBLIC_BACKEND_URL=$NEXT_PUBLIC_BACKEND_URL

# Copiar solo package.json para aprovechar cache si no hay cambios en dependencias
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código (esto invalida la cache si cambias page.tsx o componentes)
COPY . .

# Ejecutar build de producción
RUN npm run build

# Etapa 2: Producción
FROM node:18-alpine

WORKDIR /app

# Solo copiar archivos necesarios para producción
COPY --from=builder /app/.next .next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/package-lock.json* ./

# Instalar solo dependencias de producción
RUN npm install --omit=dev

# Variables configurables desde ECS o GitHub Actions
ENV PORT=3000

EXPOSE 3000

# Ejecutar la app
CMD ["npm", "start"]