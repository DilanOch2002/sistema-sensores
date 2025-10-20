# sensor-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el contenido de sensor-service al contenedor
COPY . .

CMD ["python", "app.py"]
