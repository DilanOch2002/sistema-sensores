# auth-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copia los requirements de este servicio
COPY requirements.txt .

# Actualiza pip e instala dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del servicio
COPY . .

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar
CMD ["python", "app.py"]
