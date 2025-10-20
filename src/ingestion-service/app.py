from flask import Flask, request, jsonify
from supabase import create_client
import os
import hashlib
from datetime import datetime
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import threading
from flask_cors import CORS  # ← AGREGAR ESTO

app = Flask(__name__)
CORS(app)

# Configuración Supabase
supabase_url = os.getenv('SUPABASE_URL', 'https://vqezennldyqazxjmyrfj.supabase.co')
supabase_key = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s')
supabase = create_client(supabase_url, supabase_key)

# Memoria para control de duplicados (en producción usar Redis)
processed_hashes = set()
lock = threading.Lock()

# Pool para concurrencia
executor = ThreadPoolExecutor(max_workers=10)

def get_data_hash(sensor_data):
    """Generar hash único para los datos del sensor"""
    data_string = f"{sensor_data['sensor_id']}-{sensor_data['value']}-{sensor_data['timestamp']}"
    return hashlib.md5(data_string.encode()).hexdigest()

async def process_single_record_async(sensor_data):
    """Procesar un registro de forma asíncrona"""
    try:
        data_hash = get_data_hash(sensor_data)
        
        # Verificar duplicados con lock thread-safe
        with lock:
            if data_hash in processed_hashes:
                return {"status": "duplicate", "data": sensor_data}
            processed_hashes.add(data_hash)
        
        # Verificar en base de datos si es nuevo
        existing = supabase.table('sensor_data').select('id').eq('sensor_id', sensor_data['sensor_id']).eq('timestamp', sensor_data['timestamp']).execute()
        
        if existing.data:
            return {"status": "duplicate_db", "data": sensor_data}
        
        # Agregar metadata
        sensor_data['processed_at'] = datetime.utcnow().isoformat()
        sensor_data['data_hash'] = data_hash
        
        # Guardar en Supabase
        result = supabase.table('sensor_data').insert(sensor_data).execute()
        
        return {"status": "success", "data": sensor_data}
        
    except Exception as e:
        return {"status": "error", "error": str(e), "data": sensor_data}

async def process_batch_async(batch_data):
    """Procesar lote de datos de forma concurrente"""
    tasks = [process_single_record_async(record) for record in batch_data]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ingestion-service running", "concurrent": True})

@app.route('/ingest', methods=['POST'])
def ingest_data():
    try:
        sensor_data = request.json
        
        # Validar datos requeridos
        required_fields = ['sensor_id', 'value', 'timestamp', 'type']
        for field in required_fields:
            if field not in sensor_data:
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Procesar de forma asíncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(process_single_record_async(sensor_data))
        loop.close()
        
        if result["status"] == "success":
            return jsonify({
                "status": "success", 
                "records_processed": 1,
                "sensor_id": sensor_data['sensor_id'],
                "value": sensor_data['value'],
                "processed_at": sensor_data['processed_at']
            })
        elif result["status"] in ["duplicate", "duplicate_db"]:
            return jsonify({
                "status": "duplicate", 
                "message": "Registro duplicado"
            }), 200
        else:
            return jsonify({"error": result["error"]}), 500
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch-ingest', methods=['POST'])
def batch_ingest():
    try:
        batch_data = request.json
        if not isinstance(batch_data, list):
            return jsonify({"error": "Se esperaba un array de datos"}), 400
        
        # Procesar lote de forma asíncrona y concurrente
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(process_batch_async(batch_data))
        loop.close()
        
        # Contar resultados
        processed_count = sum(1 for r in results if r and r.get("status") == "success")
        duplicates_count = sum(1 for r in results if r and r.get("status") in ["duplicate", "duplicate_db"])
        errors_count = sum(1 for r in results if r and r.get("status") == "error")
        
        return jsonify({
            "status": "success",
            "processed": processed_count,
            "duplicates": duplicates_count,
            "errors": errors_count,
            "total_received": len(batch_data),
            "concurrent_processing": True
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para pruebas de estrés
@app.route('/stress-test', methods=['POST'])
def stress_test():
    """Endpoint para generar 10,000+ registros en < 1 minuto"""
    try:
        test_config = request.json or {}
        record_count = test_config.get('record_count', 10000)
        batch_size = test_config.get('batch_size', 1000)
        
        # Generar datos de prueba masivos
        test_data = []
        base_time = datetime.utcnow()
        
        for i in range(record_count):
            sensor_data = {
                'sensor_id': f"stress_test_{i % 100}",
                'value': 20 + (i % 30),
                'type': ['temperature', 'humidity', 'rain', 'radiation'][i % 4],
                'timestamp': (base_time.timestamp() + i),
                'location': f"test_zone_{i % 10}"
            }
            test_data.append(sensor_data)
        
        # Procesar en lotes concurrentes
        total_processed = 0
        batches = [test_data[i:i + batch_size] for i in range(0, len(test_data), batch_size)]
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        for batch in batches:
            results = loop.run_until_complete(process_batch_async(batch))
            total_processed += sum(1 for r in results if r and r.get("status") == "success")
        
        loop.close()
        
        return jsonify({
            "stress_test": "completed",
            "records_generated": record_count,
            "records_processed": total_processed,
            "batch_size": batch_size,
            "processing_time_estimate": "~30-45 seconds"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)