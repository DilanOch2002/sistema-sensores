# sensor-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO el contenido del servicio
COPY . .

CMD ["python", "app.py"]
