import React, { useState, useEffect } from 'react';
import { sensorsAPI } from '../services/api';

const Dashboard = () => {
  const [sensorData, setSensorData] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('🎯 Dashboard montado, iniciando fetch...');
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    console.log('🔄 Ejecutando fetchDashboardData...');
    try {
      const data = await sensorsAPI.getLatest();
      console.log('📈 Datos para dashboard:', data);
      
      setSensorData(data.sensors || []);
      
      if (data.sensors && data.sensors.length > 0) {
        const temps = data.sensors.map(s => s.temperature).filter(t => t != null);
        const humidities = data.sensors.map(s => s.humidity).filter(h => h != null);
        
        setStats({
          avgTemp: temps.length ? (temps.reduce((a, b) => a + b) / temps.length).toFixed(1) : 'N/A',
          avgHumidity: humidities.length ? (humidities.reduce((a, b) => a + b) / humidities.length).toFixed(1) : 'N/A',
          totalSensors: data.sensors.length
        });
      } else {
        console.log('⚠️ No hay datos de sensores');
      }
    } catch (error) {
      console.error('❌ Error en fetchDashboardData:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Cargando datos en tiempo real...</div>;

  return (
    <div className="dashboard">
      <h2>🌡️ Dashboard en Tiempo Real</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>🌡️ Temp. Promedio</h3>
          <p className="stat-value">{stats.avgTemp}°C</p>
        </div>
        <div className="stat-card">
          <h3>💧 Humedad Promedio</h3>
          <p className="stat-value">{stats.avgHumidity}%</p>
        </div>
        <div className="stat-card">
          <h3>📡 Sensores Activos</h3>
          <p className="stat-value">{stats.totalSensors}</p>
        </div>
      </div>

      <div className="sensors-table">
        <h3>📊 Últimas Lecturas</h3>
        <table>
          <thead>
            <tr>
              <th>Sensor ID</th>
              <th>Temperatura</th>
              <th>Humedad</th>
              <th>Lluvia</th>
              <th>Radiación</th>
              <th>Última Actualización</th>
            </tr>
          </thead>
          <tbody>
            {sensorData.map(sensor => (
              <tr key={sensor.sensor_id}>
                <td>{sensor.sensor_id}</td>
                <td>{sensor.temperature}°C</td>
                <td>{sensor.humidity}%</td>
                <td>{sensor.rain}mm</td>
                <td>{sensor.solar_radiation}W/m²</td>
                <td>{new Date(sensor.timestamp).toLocaleTimeString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {sensorData.length === 0 && (
          <p style={{textAlign: 'center', color: '#666', padding: '2rem'}}>
            No hay datos de sensores disponibles
          </p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;