FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# ELIMINA esta línea: COPY .env .

CMD ["python", "main.py"]