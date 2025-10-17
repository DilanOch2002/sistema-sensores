import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import SensorCharts from './components/SensorCharts';
import PlotMap from './components/PlotMap';
import DeletedPlotsList from './components/DeletedPlotsList';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌱 Dashboard Agrícola IoT</h1>
        <nav className="nav-tabs">
          <button 
            className={activeTab === 'dashboard' ? 'active' : ''} 
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </button>
          <button 
            className={activeTab === 'charts' ? 'active' : ''} 
            onClick={() => setActiveTab('charts')}
          >
            📈 Gráficos
          </button>
          <button 
            className={activeTab === 'map' ? 'active' : ''} 
            onClick={() => setActiveTab('map')}
          >
            🗺️ Mapa
          </button>
          <button 
            className={activeTab === 'deleted' ? 'active' : ''} 
            onClick={() => setActiveTab('deleted')}
          >
            🗑️ Parcelas Eliminadas
          </button>
        </nav>
      </header>

      <main className="app-main">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'charts' && <SensorCharts />}
        {activeTab === 'map' && <PlotMap />}
        {activeTab === 'deleted' && <DeletedPlotsList />}
      </main>
    </div>
  );
}

export default App;