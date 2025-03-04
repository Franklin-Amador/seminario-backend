FROM python:3.9

WORKDIR /app

# Instalar Node.js (necesario para Prisma)
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Instalar Prisma CLI globalmente
RUN npm install -g prisma

# Copiar requirements.txt y archivo de schema de Prisma
COPY requirements.txt .
COPY ./prisma/ ./prisma/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código fuente
COPY . .

# Generar cliente Prisma
RUN cd prisma && prisma generate

# Exponer el puerto donde correrá la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]