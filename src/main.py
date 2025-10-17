import asyncio
import random
import time
from supabase import create_client
import os
from dotenv import load_dotenv
from datetime import datetime
import aiohttp
import json

load_dotenv()

print("🚀 Servicio B - Sensores Emulados Avanzado (Asíncrono)")

# Configuración
SUPABASE_URL = 'https://vqezennldyqazxjmyrfj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZxZXplbm5sZHlxYXp4am15cmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAyNTUzNjIsImV4cCI6MjA3NTgzMTM2Mn0.TSuCHoKKabXAQ2FlRn7BFYa_ii7WKBSBrkRr8xsuf5s'

class AdvancedSensorEmulator:
    def __init__(self):
        self.sensors = []
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
        self.ingestion_service_url = "http://ingestion-service:5001"  # Para Kubernetes
        
    def generate_sensors(self, count=50):
        """Genera sensores virtuales con ubicaciones en México"""
        print(f"🎯 Generando {count} sensores virtuales...")
        
        # Rangos aproximados de México
        locations = [
            {"city": "CDMX", "lat": 19.4326, "lon": -99.1332},
            {"city": "Guadalajara", "lat": 20.6597, "lon": -103.3496},
            {"city": "Monterrey", "lat": 25.6866, "lon": -100.3161},
            {"city": "Puebla", "lat": 19.0414, "lon": -98.2063},
            {"city": "Cancún", "lat": 21.1619, "lon": -86.8515},
        ]
        
        sensor_types = ['temperature', 'humidity', 'rain', 'solar_radiation']
        
        for i in range(count):
            location = random.choice(locations)
            sensor_type = sensor_types[i % len(sensor_types)]
            
            # Valores iniciales realistas según tipo
            if sensor_type == 'temperature':
                base_value = random.uniform(15, 35)
            elif sensor_type == 'humidity':
                base_value = random.uniform(40, 80)
            elif sensor_type == 'rain':
                base_value = random.uniform(0, 10)
            else:  # solar_radiation
                base_value = random.uniform(200, 1000)
            
            sensor = {
                'sensor_id': f"sensor_{sensor_type}_{i:03d}",
                'type': sensor_type,
                'value': round(base_value, 2),
                'latitude': location['lat'] + random.uniform(-0.5, 0.5),
                'longitude': location['lon'] + random.uniform(-0.5, 0.5),
                'city': location['city'],
                'timestamp': datetime.utcnow().isoformat(),
                'unit': self.get_unit(sensor_type)
            }
            self.sensors.append(sensor)
        
        print(f"✅ {len(self.sensors)} sensores generados")
        print(f"📊 Distribución: {[s['type'] for s in self.sensors].count('temperature')} temp, "
              f"{[s['type'] for s in self.sensors].count('humidity')} humidity, "
              f"{[s['type'] for s in self.sensors].count('rain')} rain, "
              f"{[s['type'] for s in self.sensors].count('solar_radiation')} radiation")
    
    def get_unit(self, sensor_type):
        units = {
            'temperature': '°C',
            'humidity': '%',
            'rain': 'mm',
            'solar_radiation': 'W/m²'
        }
        return units.get(sensor_type, 'units')
    
    def update_sensors_realistic(self):
        """Actualiza valores de sensores de forma realista y correlacionada"""
        current_hour = datetime.utcnow().hour
        
        for sensor in self.sensors:
            sensor_type = sensor['type']
            old_value = sensor['value']
            
            if sensor_type == 'temperature':
                # Temperatura más alta al medio día
                hour_factor = abs(12 - current_hour) / 12  # 0 al medio día, 1 a medianoche
                base_change = random.uniform(-0.3, 0.3) - (hour_factor * 0.2)
                sensor['value'] = round(max(10, min(45, old_value + base_change)), 2)
                
            elif sensor_type == 'humidity':
                # Humedad inversa a temperatura
                temp_change = abs(sensor['value'] - old_value) if sensor_type == 'temperature' else 0
                base_change = random.uniform(-1, 1) - (temp_change * 0.5)
                sensor['value'] = round(max(20, min(95, old_value + base_change)), 2)
                
            elif sensor_type == 'rain':
                # Lluvia ocasional
                if random.random() < 0.05:  # 5% de probabilidad de lluvia
                    sensor['value'] = round(random.uniform(1, 15), 2)
                else:
                    sensor['value'] = round(max(0, old_value - 0.1), 2)
                    
            elif sensor_type == 'solar_radiation':
                # Radiación solar según hora del día
                if 6 <= current_hour <= 18:  # Día
                    hour_intensity = 1 - abs(12 - current_hour) / 6  # Máximo al medio día
                    base_value = random.uniform(300, 1000) * hour_intensity
                else:  # Noche
                    base_value = random.uniform(0, 50)
                sensor['value'] = round(base_value, 2)
            
            sensor['timestamp'] = datetime.utcnow().isoformat()
    
    async def send_to_ingestion_service(self, sensor_data):
        """Envía datos al servicio de ingesta de forma asíncrona"""
        try:
            # Formatear para el servicio C
            ingestion_data = {
                'sensor_id': sensor_data['sensor_id'],
                'value': sensor_data['value'],
                'type': sensor_data['type'],
                'timestamp': datetime.utcnow().timestamp(),
                'location': sensor_data['city'],
                'unit': sensor_data['unit']
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ingestion_service_url}/ingest",
                    json=ingestion_data,
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('status') == 'success':
                            return True
            return False
            
        except Exception as e:
            print(f"❌ Error enviando a ingesta: {e}")
            return False
    
    async def send_direct_to_supabase(self, sensor_data):
        """Envía directamente a Supabase (fallback)"""
        if not self.supabase:
            return False
            
        try:
            result = self.supabase.table('sensor_data').insert({
                'sensor_id': sensor_data['sensor_id'],
                'value': sensor_data['value'],
                'type': sensor_data['type'],
                'timestamp': sensor_data['timestamp'],
                'location': sensor_data['city'],
                'unit': sensor_data['unit']
            }).execute()
            
            if result.data:
                print(f"✅ {sensor_data['sensor_id']}: {sensor_data['value']} {sensor_data['unit']}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error Supabase directo: {e}")
            return False
    
    async def sensor_worker(self, sensor, interval):
        """Worker asíncrono para cada sensor"""
        while True:
            try:
                # Actualizar valor
                self.update_sensors_realistic()
                current_data = next((s for s in self.sensors if s['sensor_id'] == sensor['sensor_id']), None)
                
                if current_data:
                    # Intentar enviar al servicio C primero
                    success = await self.send_to_ingestion_service(current_data)
                    
                    # Fallback a Supabase directo
                    if not success:
                        await self.send_direct_to_supabase(current_data)
                
                # Intervalo dinámico (1-5 segundos)
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"❌ Error en worker {sensor['sensor_id']}: {e}")
                await asyncio.sleep(5)
    
    async def run_stress_test(self, duration=60, sensor_count=200):
        """Prueba de estrés: 10,000+ registros en < 1 minuto"""
        print(f"🎯 INICIANDO PRUEBA DE ESTRÉS: {sensor_count} sensores por {duration} segundos")
        
        # Generar sensores de prueba
        test_sensors = []
        for i in range(sensor_count):
            sensor_type = ['temperature', 'humidity', 'rain', 'solar_radiation'][i % 4]
            test_sensors.append({
                'sensor_id': f"stress_{sensor_type}_{i:04d}",
                'type': sensor_type,
                'value': round(random.uniform(10, 40), 2),
                'city': 'stress_test',
                'timestamp': datetime.utcnow().isoformat(),
                'unit': self.get_unit(sensor_type)
            })
        
        start_time = time.time()
        records_sent = 0
        batch_size = 50
        
        while time.time() - start_time < duration:
            # Actualizar valores
            for sensor in test_sensors:
                sensor['value'] += random.uniform(-1, 1)
                sensor['value'] = max(0, sensor['value'])
                sensor['timestamp'] = datetime.utcnow().isoformat()
            
            # Enviar en lotes concurrentes
            tasks = []
            for i in range(0, len(test_sensors), batch_size):
                batch = test_sensors[i:i + batch_size]
                for sensor in batch:
                    tasks.append(self.send_direct_to_supabase(sensor))
                    records_sent += 1
            
            # Ejecutar concurrentemente
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Pequeña pausa
            await asyncio.sleep(0.1)
            
            # Progress update
            elapsed = time.time() - start_time
            if elapsed > 0:
                rate = records_sent / elapsed
                print(f"📊 Estrés: {records_sent} registros ({rate:.1f} reg/seg)")
        
        total_time = time.time() - start_time
        print(f"🎉 PRUEBA DE ESTRÉS COMPLETADA")
        print(f"📈 Total registros: {records_sent}")
        print(f"⏱️  Tiempo total: {total_time:.1f} segundos")
        print(f"🚀 Velocidad: {records_sent/total_time:.1f} registros/segundo")
        
        return records_sent
    
    async def start_normal_operation(self, sensor_count=20):
        """Operación normal con sensores asíncronos"""
        print("🚀 Iniciando operación normal de sensores...")
        self.generate_sensors(sensor_count)
        
        # Crear workers para cada sensor con intervalos aleatorios
        tasks = []
        for sensor in self.sensors:
            interval = random.uniform(1, 5)  # 1-5 segundos
            task = asyncio.create_task(self.sensor_worker(sensor, interval))
            tasks.append(task)
        
        print(f"📡 {len(tasks)} workers de sensores iniciados")
        print("🎯 Sensores funcionando asíncronamente...")
        
        # Mantener corriendo
        await asyncio.gather(*tasks)

async def main():
    emulator = AdvancedSensorEmulator()
    
    # 🎯 ELIGE EL MODO DE OPERACIÓN:
    
    # 1. Operación normal (descomenta esta línea)
    await emulator.start_normal_operation(sensor_count=20)
    
    # 2. Prueba de estrés 10,000+ registros (descomenta esta línea)
    # await emulator.run_stress_test(duration=50, sensor_count=200)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Servicio B detenido por el usuario")