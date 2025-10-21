# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar paquetes de Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        libffi-dev \
        libssl-dev \
        python3-dev \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del servicio
COPY . .

# Expone el puerto
EXPOSE 5003

# Comando para iniciar el servicio
CMD ["python", "app.py"]
