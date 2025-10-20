import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { plotsAPI } from '../services/api';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './PlotMap.css'; // Opcional para estilos extra

// Configurar icono de marcador para Leaflet + React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

const PlotMap = () => {
  const [plots, setPlots] = useState([]);
  const [selectedPlot, setSelectedPlot] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPlots();
  }, []);

  const fetchPlots = async () => {
    setLoading(true);
    try {
      const data = await plotsAPI.getAll();
      setPlots(data.plots || []);
    } catch (error) {
      console.error('❌ Error fetching plots:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeletePlot = async (plot) => {
    const reason = prompt(`Ingrese la razón para eliminar la parcela "${plot.name}":`, 'Sin razón especificada');
    if (!reason) return;

    try {
      await plotsAPI.delete(plot.id, reason);
      alert(`Parcela "${plot.name}" eliminada correctamente.`);
      // Refrescar lista
      fetchPlots();
      setSelectedPlot(null);
    } catch (error) {
      console.error('❌ Error al eliminar parcela:', error);
      alert('Error al eliminar la parcela. Revisa la consola.');
    }
  };

  const defaultCenter = plots.length
    ? [plots[0].location.lat, plots[0].location.lng]
    : [19.4326, -99.1332]; // Ciudad de México como fallback

  if (loading) return <div>Cargando parcelas...</div>;

  return (
    <div className="plot-map-container">
      <h2>🗺️ Mapa de Parcelas</h2>

      <MapContainer
        center={defaultCenter}
        zoom={10}
        style={{ height: '400px', width: '100%', marginBottom: '1rem' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {plots.map((plot) => (
          <Marker
            key={plot.id}
            position={[plot.location.lat, plot.location.lng]}
            eventHandlers={{
              click: () => setSelectedPlot(plot),
            }}
          >
            <Popup>
              <strong>{plot.name}</strong>
              <br />
              {plot.crop_type} • {plot.area_hectares} ha
              <br />
              Responsable: {plot.responsible}
              <br />
              <button
                style={{ marginTop: '5px', cursor: 'pointer' }}
                onClick={() => handleDeletePlot(plot)}
              >
                🗑️ Eliminar parcela
              </button>
            </Popup>
          </Marker>
        ))}
      </MapContainer>

      {selectedPlot && (
        <div className="plot-info">
          <h3>{selectedPlot.name}</h3>
          <p>
            <strong>Cultivo:</strong> {selectedPlot.crop_type}
          </p>
          <p>
            <strong>Responsable:</strong> {selectedPlot.responsible}
          </p>
          <p>
            <strong>Área:</strong> {selectedPlot.area_hectares} hectáreas
          </p>
          <p>
            <strong>Ubicación:</strong>{' '}
            {selectedPlot.location.lat.toFixed(4)}, {selectedPlot.location.lng.toFixed(4)}
          </p>
          <button onClick={() => handleDeletePlot(selectedPlot)}>🗑️ Eliminar parcela</button>
        </div>
      )}

      <div className="plots-list">
        <h3>📋 Lista de Parcelas</h3>
        <div className="plots-grid">
          {plots.map((plot) => (
            <div
              key={plot.id}
              className={`plot-card ${selectedPlot?.id === plot.id ? 'active' : ''}`}
              onClick={() => setSelectedPlot(plot)}
            >
              <h4>{plot.name}</h4>
              <p>
                {plot.crop_type} • {plot.area_hectares} ha
              </p>
              <small>{plot.responsible}</small>
              <br />
              <button
                style={{ marginTop: '5px', cursor: 'pointer' }}
                onClick={(e) => { e.stopPropagation(); handleDeletePlot(plot); }}
              >
                🗑️ Eliminar
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PlotMap;
