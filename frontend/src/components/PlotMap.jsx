import React, { useState, useEffect } from 'react';
import { plotsAPI } from '../services/api';

const PlotMap = () => {
  const [plots, setPlots] = useState([]);
  const [selectedPlot, setSelectedPlot] = useState(null);

  useEffect(() => {
    fetchPlots();
  }, []);

  const fetchPlots = async () => {
    try {
      const data = await plotsAPI.getAll();
      setPlots(data.plots || []);
    } catch (error) {
      console.error('Error fetching plots:', error);
      // Datos de ejemplo para desarrollo
      setPlots([
        {
          id: 1,
          name: "Parcela Norte",
          location: { lat: 19.4326, lng: -99.1332 },
          crop_type: "Maíz",
          responsible: "Juan Pérez",
          area_hectares: 5.0
        },
        {
          id: 2, 
          name: "Parcela Sur",
          location: { lat: 19.3326, lng: -99.2332 },
          crop_type: "Trigo",
          responsible: "María García",
          area_hectares: 3.5
        }
      ]);
    }
  };

  return (
    <div className="plot-map">
      <h2>🗺️ Mapa de Parcelas</h2>
      
      <div className="map-container">
        {/* Mapa simulado - en producción usarías Leaflet o Google Maps */}
        <div className="simulated-map">
          <div className="map-grid">
            {plots.map(plot => (
              <div 
                key={plot.id}
                className={`map-plot ${selectedPlot?.id === plot.id ? 'selected' : ''}`}
                style={{
                  left: `${(plot.location.lng + 100) * 2}%`,
                  top: `${(plot.location.lat - 10) * 2}%`
                }}
                onClick={() => setSelectedPlot(plot)}
                title={plot.name}
              >
                🌱
              </div>
            ))}
          </div>
        </div>

        {/* Información de parcela seleccionada */}
        {selectedPlot && (
          <div className="plot-info">
            <h3>{selectedPlot.name}</h3>
            <p><strong>Cultivo:</strong> {selectedPlot.crop_type}</p>
            <p><strong>Responsable:</strong> {selectedPlot.responsible}</p>
            <p><strong>Área:</strong> {selectedPlot.area_hectares} hectáreas</p>
            <p><strong>Ubicación:</strong> {selectedPlot.location.lat.toFixed(4)}, {selectedPlot.location.lng.toFixed(4)}</p>
          </div>
        )}
      </div>

      <div className="plots-list">
        <h3>📋 Lista de Parcelas</h3>
        <div className="plots-grid">
          {plots.map(plot => (
            <div 
              key={plot.id} 
              className={`plot-card ${selectedPlot?.id === plot.id ? 'active' : ''}`}
              onClick={() => setSelectedPlot(plot)}
            >
              <h4>{plot.name}</h4>
              <p>{plot.crop_type} • {plot.area_hectares} ha</p>
              <small>{plot.responsible}</small>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PlotMap;