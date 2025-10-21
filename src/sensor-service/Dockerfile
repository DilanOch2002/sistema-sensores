FROM python:3.11-slim

WORKDIR /app

# Instala dependencias del sistema necesarias para pip
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del servicio
COPY . .

CMD ["python", "app.py"]
