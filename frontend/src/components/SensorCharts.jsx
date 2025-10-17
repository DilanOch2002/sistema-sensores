import React, { useState, useEffect, useCallback } from 'react';

const SensorCharts = () => {
  const [timeRange, setTimeRange] = useState(24); // horas

  const fetchChartData = useCallback(async () => {
    try {
      // Simular datos para desarrollo
      console.log('Fetching data for range:', timeRange);
    } catch (error) {
      console.error('Error fetching chart data:', error);
    }
  }, [timeRange]);

  useEffect(() => {
    fetchChartData();
  }, [fetchChartData]);

  // Gráficos simulados
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

  return (
    <div className="sensor-charts">
      <h2>📈 Gráficos Históricos</h2>
      
      <div className="chart-controls">
        <label>Rango de tiempo: </label>
        <select value={timeRange} onChange={(e) => setTimeRange(Number(e.target.value))}>
          <option value={6}>6 horas</option>
          <option value={24}>24 horas</option>
          <option value={168}>1 semana</option>
        </select>
      </div>

      <div className="charts-grid">
        {renderChart('🌡️ Temperatura', 
          [{value: 25}, {value: 26}, {value: 24}, {value: 23}, {value: 22}], 
          '#ff6b6b'
        )}
        
        {renderChart('💧 Humedad', 
          [{value: 65}, {value: 70}, {value: 68}, {value: 72}, {value: 75}], 
          '#4ecdc4'
        )}
        
        {renderChart('🌧️ Lluvia', 
          [{value: 0}, {value: 5}, {value: 2}, {value: 0}, {value: 8}], 
          '#45b7d1'
        )}
        
        {renderChart('☀️ Radiación Solar', 
          [{value: 800}, {value: 750}, {value: 900}, {value: 600}, {value: 700}], 
          '#f9c74f'
        )}
      </div>

      <div className="chart-legend">
        <p><strong>Leyenda:</strong> Gráficos de demostración con datos simulados</p>
      </div>
    </div>
  );
};

export default SensorCharts;