FROM python:3.9
WORKDIR /app

# Add Microsoft SQL Server tools repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Pre-accept the EULA for SQL Server tools
ENV ACCEPT_EULA=Y

# Instalar Node.js y MS SQL Server client tools
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    unixodbc \
    unixodbc-dev \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools \
    && rm -rf /var/lib/apt/lists/*

# Add SQL Server tools to PATH
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && export PATH="$PATH:/opt/mssql-tools/bin"

# Instalar Prisma CLI globalmente
RUN npm install -g prisma

# Crear directorios para archivos subidos
RUN mkdir -p /app/uploads/assignments /app/uploads/resources /app/uploads/profiles

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python de manera explícita
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir python-multipart==0.0.9
RUN pip install --no-cache-dir pyodbc==4.0.34

# Copiar el resto del código fuente
COPY . .

# Copiar y generar cliente Prisma
COPY ./prisma/ ./prisma/
RUN cd prisma && prisma generate

# Exponer el puerto donde correrá la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
