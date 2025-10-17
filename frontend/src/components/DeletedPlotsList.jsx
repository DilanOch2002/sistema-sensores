import React, { useState, useEffect } from 'react';
import { plotsAPI } from '../services/api';

const DeletedPlotsList = () => {
  const [deletedPlots, setDeletedPlots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDeletedPlots();
  }, []);

  const fetchDeletedPlots = async () => {
    try {
      const data = await plotsAPI.getDeleted();
      setDeletedPlots(data.deleted_plots || []);
    } catch (error) {
      console.error('Error fetching deleted plots:', error);
      // Datos de ejemplo
      setDeletedPlots([
        {
          original_id: 3,
          name: "Parcela Este (Eliminada)",
          location: { lat: 19.5326, lng: -99.0332 },
          crop_type: "Soja", 
          responsible: "Carlos López",
          deleted_at: "2024-01-15T10:30:00Z",
          deleted_reason: "Cambio de cultivo"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Cargando historial...</div>;

  return (
    <div className="deleted-plots">
      <h2>🗑️ Parcelas Eliminadas</h2>
      <p className="subtitle">Historial de parcelas que han sido eliminadas del sistema</p>

      {deletedPlots.length === 0 ? (
        <div className="empty-state">
          <p>No hay parcelas eliminadas en el historial.</p>
        </div>
      ) : (
        <div className="deleted-plots-grid">
          {deletedPlots.map(plot => (
            <div key={plot.original_id} className="deleted-plot-card">
              <div className="plot-header">
                <h3>{plot.name}</h3>
                <span className="deleted-badge">ELIMINADA</span>
              </div>
              
              <div className="plot-details">
                <p><strong>🌾 Cultivo:</strong> {plot.crop_type}</p>
                <p><strong>👤 Responsable:</strong> {plot.responsible}</p>
                <p><strong>📍 Ubicación:</strong> {plot.location.lat.toFixed(4)}, {plot.location.lng.toFixed(4)}</p>
                <p><strong>🗓️ Eliminada el:</strong> {new Date(plot.deleted_at).toLocaleDateString()}</p>
                <p><strong>📝 Razón:</strong> {plot.deleted_reason}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default DeletedPlotsList;