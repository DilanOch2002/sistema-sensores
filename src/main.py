import requests
from supabase import create_client
import os
from dotenv import load_dotenv  # ← AÑADIDO

# ← AÑADIDO
load_dotenv()

print("🚀 Iniciando sistema de monitoreo de sensores...")

# Configuración
SENSORS_API = "https://sensores-async-api.onrender.com/api/sensors/all"
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def get_sensor_data():
    """Obtiene datos de la API de sensores"""
    print("📡 Conectando con API de sensores...")
    try:
        response = requests.get(SENSORS_API)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'temperatura' in data:
                sensor_list = data['temperatura']
                print(f"✅ Datos obtenidos: {len(sensor_list)} registros")
                return sensor_list
            else:
                print("ℹ️ La API respondió pero no en el formato esperado")
                return []
        else:
            print(f"❌ Error API: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return []

def save_to_supabase(data):
    """Guarda datos en Supabase"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Faltan credenciales de Supabase")
        return
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Insertar datos
        for sensor in data[:3]:  # Solo primeros 3 para prueba
            result = supabase.table('sensors').insert({
                'sensor_id': f"sensor_{sensor.get('value', 0)}",  # ID único
                'temperature': sensor.get('value', 0),
                'humidity': 0,
                'timestamp': sensor.get('timestamp'),
                'latitude': sensor.get('coords', {}).get('lat'),
                'longitude': sensor.get('coords', {}).get('lon')
            }).execute()
            print(f"✅ Sensor {sensor.get('value')} guardado")
            
    except Exception as e:
        print(f"❌ Error guardando en Supabase: {e}")

if __name__ == "__main__":
    print("🎯 Iniciando recolección de datos...")
    
    # Obtener datos
    sensor_data = get_sensor_data()
    
    if sensor_data:
        # Guardar en base de datos
        save_to_supabase(sensor_data)
        print("🎉 Proceso completado exitosamente!")
    else:
        print("😞 No se pudieron obtener datos")