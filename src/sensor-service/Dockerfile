# Base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar paquetes de Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ \
        libffi-dev \
        libssl-dev \
        python3-dev \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Actualiza pip e instala dependencias de Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del servicio
COPY . .

# Expone puerto
EXPOSE 5003

# Comando de inicio
CMD ["python", "app.py"]
