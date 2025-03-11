FROM python:3.12

WORKDIR /app

# Instalar Node.js y PostgreSQL client
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instalar Prisma CLI globalmente
RUN npm install -g prisma

# Crear directorios para archivos subidos
RUN mkdir -p /app/uploads/assignments /app/uploads/resources /app/uploads/profiles

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python de manera explícita
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-multipart==0.0.9

# Copiar el resto del código fuente
COPY . .

# Copiar y generar cliente Prisma
COPY ./prisma/ ./prisma/
RUN cd prisma && prisma generate

# Exponer el puerto donde correrá la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]