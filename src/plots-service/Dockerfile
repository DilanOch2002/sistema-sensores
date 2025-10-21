FROM python:3.11-slim

WORKDIR /app

# Copia el requirements desde la raíz
COPY ../../requirements.txt .

# Actualiza pip e instala dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del servicio
COPY . .

CMD ["python", "app.py"]
