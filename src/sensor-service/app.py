from flask import Flask, jsonify
import asyncio
import random
from datetime import datetime, timedelta
from threading import Thread
import time
from flask_cors import CORS  # ← AGREGAR ESTO

app = Flask(__name__)
CORS(app)

# Datos simulados para el frontend
sensor_data_cache = []
last_updated = None

def generate_sensor_data():
    """Generar datos de sensores simulados"""
    global sensor_data_cache, last_updated
    
    sensors = []
    base_time = datetime.utcnow()
    
    # Generar 15 sensores de ejemplo
    for i in range(15):
        sensor_type = ['temperature', 'humidity', 'rain', 'solar_radiation'][i % 4]
        
        if sensor_type == 'temperature':
            value = round(random.uniform(20, 35), 1)
        elif sensor_type == 'humidity':
            value = round(random.uniform(40, 85), 1)
        elif sensor_type == 'rain':
            value = round(random.uniform(0, 12), 1)
        else:
            value = round(random.uniform(200, 950), 1)
        
        sensor = {
            'sensor_id': f"sensor_{sensor_type}_{i:02d}",
            'temperature': value if sensor_type == 'temperature' else round(random.uniform(20, 35), 1),
            'humidity': value if sensor_type == 'humidity' else round(random.uniform(40, 85), 1),
            'rain': value if sensor_type == 'rain' else round(random.uniform(0, 5), 1),
            'solar_radiation': value if sensor_type == 'solar_radiation' else round(random.uniform(300, 900), 1),
            'timestamp': (base_time - timedelta(minutes=random.randint(0, 60))).isoformat(),
            'latitude': 19.4326 + random.uniform(-0.5, 0.5),
            'longitude': -99.1332 + random.uniform(-0.5, 0.5)
        }
        sensors.append(sensor)
    
    sensor_data_cache = sensors
    last_updated = datetime.utcnow()
    return sensors

def update_sensor_data():
    """Actualizar datos cada 30 segundos en segundo plano"""
    while True:
        generate_sensor_data()
        time.sleep(30)

# Endpoints HTTP para el frontend
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "sensors-service running", "http": True})

@app.route('/sensors/latest', methods=['GET'])
def get_latest_sensors():
    """Endpoint que tu frontend necesita"""
    if not sensor_data_cache:
        generate_sensor_data()
    
    return jsonify({"sensors": sensor_data_cache})

@app.route('/sensors/historical', methods=['GET'])
def get_historical_sensors():
    """Endpoint para datos históricos"""
    from datetime import datetime, timedelta
    
    # Simular datos históricos de las últimas 24 horas
    historical_data = []
    base_time = datetime.utcnow()
    
    for i in range(100):
        historical_data.append({
            'timestamp': (base_time - timedelta(minutes=i*15)).isoformat(),
            'temperature': round(random.uniform(18, 32), 1),
            'humidity': round(random.uniform(45, 80), 1),
            'rain': round(random.uniform(0, 8), 1),
            'solar_radiation': round(random.uniform(150, 900), 1),
            'sensor_id': f"sensor_temp_{i%10:02d}"
        })
    
    return jsonify({"historical": historical_data})

@app.route('/sensors/stats', methods=['GET'])
def get_sensor_stats():
    """Estadísticas de sensores"""
    if not sensor_data_cache:
        generate_sensor_data()
    
    temps = [s['temperature'] for s in sensor_data_cache if s['temperature']]
    humidities = [s['humidity'] for s in sensor_data_cache if s['humidity']]
    
    return jsonify({
        "total_sensors": len(sensor_data_cache),
        "avg_temperature": round(sum(temps) / len(temps), 2) if temps else 0,
        "avg_humidity": round(sum(humidities) / len(humidities), 2) if humidities else 0,
        "last_updated": last_updated.isoformat() if last_updated else None
    })

if __name__ == '__main__':
    # Generar datos iniciales
    generate_sensor_data()
    
    # Iniciar hilo para actualizar datos en segundo plano
    update_thread = Thread(target=update_sensor_data, daemon=True)
    update_thread.start()
    
    print("🚀 Sensors Service HTTP iniciado en puerto 5003")
    app.run(host='0.0.0.0', port=5003, debug=False)