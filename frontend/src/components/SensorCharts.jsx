import React, { useState, useEffect, useCallback } from 'react';
import { sensorsAPI } from '../services/api';

const SensorCharts = () => {
  const [timeRange, setTimeRange] = useState(24); // horas
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchChartData = useCallback(async () => {
    setLoading(true);
    try {
      const data = await sensorsAPI.getHistorical(timeRange);
      setChartData(data.historical || []);
    } catch (error) {
      console.error('❌ Error fetching sensor historical data:', error);
      setChartData([]);
    } finally {
      setLoading(false);
    }
  }, [timeRange]);

  useEffect(() => {
    fetchChartData();
  }, [fetchChartData]);

  // Transformar datos para los gráficos (últimos 20 registros)
  const getChartData = (type) => {
    if (!chartData) return [];
    return chartData.slice(-20).map(item => ({
      timestamp: item.timestamp,
      value: item[type] || 0
    }));
  };

  const renderChart = (title, data, color) => (
    <div className="chart-container">
      <h3>{title}</h3>
      <div className="chart-bars">
        {data.map((item, index) => (
          <div
            key={index}
            className="chart-bar"
            style={{ 
              height: `${item.value}%`, 
              backgroundColor: color 
            }}
            title={`${item.value}`}
          >
            <span className="bar-label">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );

  if (loading) return <div>Cargando gráficos de sensores...</div>;

  return (
    <div className="sensor-charts">
      <h2>📈 Gráficos Históricos de Sensores</h2>

      <div className="chart-controls">
        <label>Rango de tiempo: </label>
        <select value={timeRange} onChange={(e) => setTimeRange(Number(e.target.value))}>
          <option value={6}>6 horas</option>
          <option value={24}>24 horas</option>
          <option value={168}>1 semana</option>
        </select>
        <button onClick={fetchChartData} style={{ marginLeft: '10px' }}>
          🔄 Actualizar
        </button>
      </div>

      <div className="charts-grid">
        {chartData.length > 0 ? (
          <>
            {renderChart('🌡️ Temperatura', getChartData('temperature'), '#ff6b6b')}
            {renderChart('💧 Humedad', getChartData('humidity'), '#4ecdc4')}
            {renderChart('🌧️ Lluvia', getChartData('rain'), '#45b7d1')}
            {renderChart('☀️ Radiación Solar', getChartData('solar_radiation'), '#f9c74f')}
          </>
        ) : (
          <p>No hay datos históricos disponibles</p>
        )}
      </div>

      <div className="chart-legend">
        <p><strong>Leyenda:</strong> Datos reales de sensores cargados desde el backend</p>
      </div>
    </div>
  );
};

export default SensorCharts;
